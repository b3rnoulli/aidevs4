"""Register the find-cities tool with Centrala for the `negotiations` task.

Steps:
  1. Sanity-check the local tool (POST /api/find-cities) is reachable through
     ngrok (the URL is read from NGROK_URL or hard-coded fallback).
  2. Submit the single-tool spec to /verify (task=negotiations).
  3. Poll /verify with action=check until Centrala finishes its async
     evaluation and returns the flag.
"""
from __future__ import annotations

import json
import os
import sys
import time

import requests
from dotenv import load_dotenv

from aidevs4.centrala import submit_answer

NGROK_URL = os.environ.get(
    "NGROK_URL", "https://1291-103-11-50-118.ngrok-free.app"
).rstrip("/")
TOOL_PATH = "/api/find-cities"
TOOL_URL = f"{NGROK_URL}{TOOL_PATH}"

TOOL_DESCRIPTION = (
    "Zwraca miasta sprzedajace JEDEN przedmiot. params: opis po polsku "
    "(np. 'turbina wiatrowa 48V', 'inwerter 3000W', 'akumulator AGM'). "
    "output: 'Nazwa: miasto1, miasto2'. Aby znalezc miasta majace "
    "WSZYSTKIE potrzebne przedmioty, odpytaj osobno dla kazdego i policz "
    "przeciecie zbiorow miast."
)


def sanity_check() -> None:
    print(f"sanity-checking {TOOL_URL}")
    try:
        r = requests.post(
            TOOL_URL,
            json={"params": "Turbina wiatrowa 400W 48V"},
            timeout=15,
            headers={"ngrok-skip-browser-warning": "true"},
        )
        r.raise_for_status()
        data = r.json()
    except (requests.RequestException, ValueError) as exc:
        sys.exit(f"sanity-check failed: {exc}\nIs the server running on port 3000?")
    print(f"  response: {data}")
    if "output" not in data or len(data["output"].encode("utf-8")) > 500:
        sys.exit(f"unexpected sanity response: {data!r}")


def register() -> dict:
    answer = {
        "tools": [
            {"URL": TOOL_URL, "description": TOOL_DESCRIPTION},
        ]
    }
    print(f"registering tool: {TOOL_URL}")
    print(f"description ({len(TOOL_DESCRIPTION)} chars): {TOOL_DESCRIPTION}")
    return submit_answer("negotiations", answer)


def poll_check(max_attempts: int = 12, delay: float = 15.0) -> dict:
    for attempt in range(1, max_attempts + 1):
        print(f"\ncheck attempt {attempt}/{max_attempts} (waited ~{(attempt - 1) * delay:.0f}s)")
        try:
            result = submit_answer("negotiations", {"action": "check"})
        except requests.HTTPError as exc:
            body = exc.response.text if exc.response is not None else ""
            print(f"  HTTP error: {exc}\n{body}")
            time.sleep(delay)
            continue

        print(f"  {json.dumps(result, ensure_ascii=False)}")
        text = json.dumps(result, ensure_ascii=False)
        if "FLG" in text:
            return result
        if result.get("code") not in (0, None):
            # non-zero usually means still running; keep polling
            pass
        time.sleep(delay)
    raise SystemExit("did not receive flag in time")


def main() -> None:
    load_dotenv()
    sanity_check()
    response = register()
    print(f"register response: {json.dumps(response, ensure_ascii=False, indent=2)}")
    print("\nwaiting 30s before first check (Centrala runs the agent async)…")
    time.sleep(30)
    flag = poll_check()
    print(f"\nFLAG: {json.dumps(flag, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
