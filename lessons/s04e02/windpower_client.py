"""Thin one-shot client for the S04E02 `windpower` API.

Each invocation POSTs ONE action to /verify with task=windpower and prints
the JSON response. Used to probe the API manually before running the timed
solver. Examples:

    uv run python lessons/s04e02/windpower_client.py help
    uv run python lessons/s04e02/windpower_client.py getResult
    uv run python lessons/s04e02/windpower_client.py start
    uv run python lessons/s04e02/windpower_client.py raw '{"action":"unlockCodeGenerator","input":"foo"}'
"""
from __future__ import annotations

import json
import os
import sys

from dotenv import load_dotenv

from aidevs4.centrala import submit_answer

TASK_NAME = "windpower"


def main() -> int:
    load_dotenv()
    if len(sys.argv) < 2:
        print("usage: windpower_client.py <action> [k=v ...]")
        print("       windpower_client.py raw '<json answer object>'")
        return 2

    if sys.argv[1] == "raw":
        if len(sys.argv) < 3:
            print("missing JSON object")
            return 2
        answer = json.loads(sys.argv[2])
    else:
        action = sys.argv[1]
        answer: dict = {"action": action}
        for arg in sys.argv[2:]:
            if "=" not in arg:
                print(f"ignoring arg without '=': {arg}")
                continue
            k, v = arg.split("=", 1)
            # try parse as int / float / json
            try:
                v_parsed = json.loads(v)
            except json.JSONDecodeError:
                v_parsed = v
            answer[k] = v_parsed

    result = submit_answer(TASK_NAME, answer)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
