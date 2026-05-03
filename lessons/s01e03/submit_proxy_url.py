import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from aidevs4.centrala import submit_answer

DEFAULT_URL = "https://3e2b-103-11-50-118.ngrok-free.app/"
DEFAULT_SESSION_ID = "hub-test-1"


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    load_dotenv(repo_root / ".env")
    load_dotenv()

    parser = argparse.ArgumentParser(description="Submit proxy URL to centrala")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--session-id", default=DEFAULT_SESSION_ID)
    args = parser.parse_args()

    answer = {"url": args.url, "sessionID": args.session_id}
    print(f"Submitting: {answer}")
    result = submit_answer("proxy", answer)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
