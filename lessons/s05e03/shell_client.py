"""Thin client for the S05E03 `shellaccess` task.

Each invocation sends ONE shell command to Centrala via /verify and prints
the parsed JSON response. We drive the exploration interactively from Bash.

Usage:
    uv run python lessons/s05e03/shell_client.py "<command>"
    uv run python lessons/s05e03/shell_client.py 'echo {"date":"...","city":"...","longitude":...,"latitude":...}'
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

from aidevs4.centrala import submit_answer

LESSON_DIR = Path(__file__).resolve().parent
SESSION_LOG = LESSON_DIR / "session.log"

TASK_NAME = "shellaccess"


def load_env() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    load_dotenv(repo_root / ".env")
    load_dotenv(repo_root.parent.parent.parent / ".env")


def log(cmd: str, response: dict) -> None:
    with SESSION_LOG.open("a", encoding="utf-8") as fh:
        fh.write(f"$ {cmd}\n")
        fh.write(json.dumps(response, ensure_ascii=False, indent=2) + "\n\n")


def run(cmd: str) -> dict:
    time.sleep(0.4)  # gentle pacing — these endpoints rate-limit
    try:
        return submit_answer(TASK_NAME, {"cmd": cmd})
    except requests.HTTPError as e:
        body = e.response.text if e.response is not None else str(e)
        try:
            return json.loads(body)
        except (ValueError, TypeError):
            return {"http_error": str(e), "raw": body}


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: shell_client.py <command...>", file=sys.stderr)
        print("       shell_client.py --submit-json '{\"date\":...}'", file=sys.stderr)
        return 2

    load_env()
    if not os.environ.get("CENTRALA_API_KEY"):
        print("CENTRALA_API_KEY missing", file=sys.stderr)
        return 2

    if sys.argv[1] == "--submit-json":
        if len(sys.argv) < 3:
            print("missing JSON payload", file=sys.stderr)
            return 2
        # Validate then re-encode compactly to avoid stray spaces; wrap in
        # single-quoted echo on the remote shell so braces/commas don't get
        # expanded and our quoted JSON survives intact.
        payload = json.loads(sys.argv[2])
        compact = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        # Escape any single quotes inside the JSON for the single-quoted shell string.
        escaped = compact.replace("'", "'\\''")
        cmd = f"echo '{escaped}'"
    else:
        cmd = " ".join(sys.argv[1:])

    response = run(cmd)
    log(cmd, response)
    print(json.dumps(response, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
