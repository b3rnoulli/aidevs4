import os
from typing import Any

import requests


def submit_answer(
    task: str,
    answer: Any,
    *,
    api_key: str | None = None,
    base_url: str = "https://hub.ag3nts.org",
) -> dict:
    key = api_key or os.environ["CENTRALA_API_KEY"]
    payload = {"apikey": key, "task": task, "answer": answer}
    response = requests.post(f"{base_url}/verify", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
