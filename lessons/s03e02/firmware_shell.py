"""Thin client for the S03E02 `firmware` shell API.

Usage:
    uv run python lessons/s03e02/firmware_shell.py <command...>
    uv run python lessons/s03e02/firmware_shell.py --reboot
    uv run python lessons/s03e02/firmware_shell.py --submit ECCS-xxxxxxxx...

Each invocation sends ONE command to https://hub.ag3nts.org/api/shell with the
CENTRALA_API_KEY from .env, prints the JSON response, and exits. This keeps
each call observable so we can reason about the next step manually.

Safety rails (matched to the task description):
- Refuse any command containing /etc, /root, or /proc.
- (We also avoid touching paths from .gitignore files when we encounter them.)
"""
from __future__ import annotations

import json
import os
import sys

import requests
from dotenv import load_dotenv

from aidevs4.centrala import submit_answer

SHELL_URL = "https://hub.ag3nts.org/api/shell"
TASK_NAME = "firmware"
HARD_FORBIDDEN = ("/etc", "/root", "/proc")


def shell(cmd: str, api_key: str) -> dict:
    lc = cmd.lower()
    for root in HARD_FORBIDDEN:
        if root in lc:
            return {"refused_locally": True,
                    "reason": f"command references forbidden root '{root}'"}
    r = requests.post(SHELL_URL, json={"apikey": api_key, "cmd": cmd}, timeout=60)
    try:
        return r.json()
    except ValueError:
        return {"http_status": r.status_code, "raw": r.text}


def main() -> int:
    load_dotenv()
    api_key = os.environ["CENTRALA_API_KEY"]

    if len(sys.argv) < 2:
        print("usage: firmware_shell.py <cmd...>")
        print("       firmware_shell.py --reboot")
        print("       firmware_shell.py --submit ECCS-xxx")
        return 2

    if sys.argv[1] == "--reboot":
        print(json.dumps(shell("reboot", api_key), ensure_ascii=False, indent=2))
        return 0

    if sys.argv[1] == "--submit":
        if len(sys.argv) < 3:
            print("missing ECCS code")
            return 2
        code = sys.argv[2]
        result = submit_answer(TASK_NAME, {"confirmation": code})
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    cmd = " ".join(sys.argv[1:])
    print(json.dumps(shell(cmd, api_key), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
