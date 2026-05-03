"""Activate railway route X-01 via the self-documenting hub.ag3nts.org API.

The endpoint is intentionally flaky (503 simulated overload) and rate-limited.
This script wraps every call with retry/backoff and header-driven waits.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from email.utils import parsedate_to_datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

ENDPOINT = "https://hub.ag3nts.org/verify"
TASK = "railway"

MAX_503_RETRIES = 8
BACKOFF_BASE = 2.0
BACKOFF_CAP = 30.0
DEFAULT_PAUSE = 6.0  # safe pause between successful calls if no header info

RATE_RESET_HEADERS = ("x-ratelimit-reset", "ratelimit-reset")
RATE_REMAINING_HEADERS = ("x-ratelimit-remaining", "ratelimit-remaining")
RETRY_AFTER_HEADERS = ("retry-after",)

FLAG_RE = re.compile(r"\{FLG:[^}]+\}")


def _parse_retry_after(value: str) -> float | None:
    value = value.strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        pass
    try:
        dt = parsedate_to_datetime(value)
        return max(0.0, dt.timestamp() - time.time())
    except (TypeError, ValueError):
        return None


def _parse_reset(value: str) -> float | None:
    value = value.strip()
    if not value:
        return None
    try:
        v = float(value)
    except ValueError:
        return None
    now = time.time()
    # Heuristic: if it looks like an epoch (>= now-ish), treat as absolute.
    return max(0.0, v - now) if v > now - 60 else v


def _wait_seconds_from_headers(resp: requests.Response) -> float:
    headers = {k.lower(): v for k, v in resp.headers.items()}
    for h in RETRY_AFTER_HEADERS:
        if h in headers:
            secs = _parse_retry_after(headers[h])
            if secs is not None:
                return secs
    remaining = None
    for h in RATE_REMAINING_HEADERS:
        if h in headers:
            try:
                remaining = int(float(headers[h]))
            except ValueError:
                pass
            break
    if remaining is not None and remaining <= 0:
        for h in RATE_RESET_HEADERS:
            if h in headers:
                secs = _parse_reset(headers[h])
                if secs is not None:
                    return secs
    return 0.0


def _log(prefix: str, payload) -> None:
    if isinstance(payload, (dict, list)):
        text = json.dumps(payload, ensure_ascii=False, indent=2)
    else:
        text = str(payload)
    print(f"[{time.strftime('%H:%M:%S')}] {prefix}: {text}", flush=True)


def _interesting_headers(resp: requests.Response) -> dict:
    keys = {*RATE_RESET_HEADERS, *RATE_REMAINING_HEADERS, *RETRY_AFTER_HEADERS}
    return {k: v for k, v in resp.headers.items() if k.lower() in keys}


def verify(api_key: str, action: dict) -> dict:
    """POST one action to the railway endpoint, retrying on 503."""
    body = {"apikey": api_key, "task": TASK, "answer": action}
    _log("REQUEST", action)

    attempt = 0
    while True:
        resp = requests.post(ENDPOINT, json=body, timeout=30)
        headers_of_interest = _interesting_headers(resp)
        if headers_of_interest:
            _log("HEADERS", headers_of_interest)

        if resp.status_code == 503:
            attempt += 1
            if attempt > MAX_503_RETRIES:
                _log("ERROR", f"503 after {MAX_503_RETRIES} retries: {resp.text}")
                resp.raise_for_status()
            wait = min(BACKOFF_CAP, BACKOFF_BASE * (2 ** (attempt - 1)))
            header_wait = _wait_seconds_from_headers(resp)
            wait = max(wait, header_wait)
            _log("503", f"attempt {attempt}, sleeping {wait:.1f}s")
            time.sleep(wait)
            continue

        if resp.status_code == 429:
            wait = max(_wait_seconds_from_headers(resp), DEFAULT_PAUSE)
            _log("429", f"sleeping {wait:.1f}s; body: {resp.text}")
            time.sleep(wait)
            continue

        if not resp.ok:
            _log("HTTP_ERROR", f"{resp.status_code} body: {resp.text}")
            resp.raise_for_status()

        try:
            data = resp.json()
        except ValueError:
            _log("RESPONSE_TEXT", resp.text)
            raise

        _log("RESPONSE", data)

        # Proactively wait if rate-limit headers say we must.
        wait = _wait_seconds_from_headers(resp)
        if wait > 0:
            _log("RATE_WAIT", f"sleeping {wait:.1f}s before next call")
            time.sleep(wait)
        else:
            time.sleep(DEFAULT_PAUSE)

        return data


def find_flag(data) -> str | None:
    text = json.dumps(data, ensure_ascii=False)
    m = FLAG_RE.search(text)
    return m.group(0) if m else None


def run_help(api_key: str) -> dict:
    return verify(api_key, {"action": "help"})


def run_full(api_key: str) -> None:
    """Activate route x-01: reconfigure -> setstatus RTOPEN -> save."""
    route = "x-01"
    steps = [
        {"action": "reconfigure", "route": route},
        {"action": "setstatus", "route": route, "value": "RTOPEN"},
        {"action": "save", "route": route},
    ]

    for step in steps:
        data = verify(api_key, step)
        flag = find_flag(data)
        if flag:
            print(f"\nFLAG: {flag}")
            return

    print("\nSequence finished without a flag in any response.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Activate railway route X-01.")
    parser.add_argument("--help-only", action="store_true",
                        help="Only call the help action and print the docs.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    load_dotenv(repo_root / ".env")
    load_dotenv(repo_root.parent.parent.parent / ".env")  # main repo .env (worktree fallback)

    api_key = os.environ.get("CENTRALA_API_KEY")
    if not api_key:
        print("CENTRALA_API_KEY missing from environment", file=sys.stderr)
        return 2

    if args.help_only:
        run_help(api_key)
    else:
        run_full(api_key)
    return 0


if __name__ == "__main__":
    sys.exit(main())
