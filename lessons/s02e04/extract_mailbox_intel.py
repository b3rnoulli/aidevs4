"""Extract attack intel from a hacked operator mailbox (task: mailbox).

Searches the zmail API for the relevant threads (Wiktor's tip-off from
proton.me, the security ticket reply with the planned attack date and
SEC- confirmation code, and the password-rotation email), pulls the three
required values, and submits to /verify.

Extraction is deterministic: the patterns are well-defined (YYYY-MM-DD,
SEC-{32 hex}, password line). Gemini stays as an optional fallback when
the regex pass leaves any field empty (set USE_GEMINI=1 to enable).
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

from aidevs4.centrala import submit_answer

ZMAIL_URL = "https://hub.ag3nts.org/api/zmail"
CACHE_DIR = Path(__file__).parent / "cache"
REQUEST_DELAY = 1.5  # seconds between zmail calls (per-key rate limit is tight)

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATE_IN_TEXT_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
CONFIRMATION_RE = re.compile(r"^SEC-[A-Za-z0-9]{32}$")
CONFIRMATION_IN_TEXT_RE = re.compile(r"SEC-[A-Za-z0-9]{32}")
PASSWORD_LINE_RE = re.compile(
    r"(?:hasłem|hasło)\s*:\s*\n?\s*([A-Za-z0-9_!@#$%^&*+\-=.]+)",
    re.IGNORECASE,
)

SEARCH_QUERIES = [
    "from:proton.me",
    "subject:SEC",
    "hasło OR password",
]

ATTACK_KEYWORDS = ("zbombard", "bombard", "atak", "uderz")


def zmail(action: str, **params: Any) -> dict:
    payload = {"apikey": os.environ["CENTRALA_API_KEY"], "action": action, **params}
    for attempt in range(5):
        time.sleep(REQUEST_DELAY)
        response = requests.post(ZMAIL_URL, json=payload, timeout=30)
        if response.status_code == 429:
            wait = 10 * (attempt + 1)
            print(f"  zmail HTTP 429 — sleeping {wait}s")
            time.sleep(wait)
            continue
        response.raise_for_status()
        data = response.json()
        if not data.get("ok"):
            if data.get("code") == -9999:
                wait = 15 * (attempt + 1)
                print(f"  zmail rate-limited (code -9999) — sleeping {wait}s")
                time.sleep(wait)
                continue
            raise RuntimeError(f"zmail {action} failed: {data}")
        return data
    raise RuntimeError(f"zmail {action} exhausted retries")


def collect_messages() -> list[dict]:
    CACHE_DIR.mkdir(exist_ok=True)
    cached: dict[str, dict] = {}
    for path in CACHE_DIR.glob("msg_*.json"):
        msg = json.loads(path.read_text())
        cached[msg["messageID"]] = msg

    found_ids: set[str] = set()
    thread_ids: set[int] = set()

    for query in SEARCH_QUERIES:
        page = 1
        while True:
            data = zmail("search", query=query, perPage=20, page=page)
            for item in data["items"]:
                found_ids.add(item["messageID"])
                if item.get("threadID") is not None:
                    thread_ids.add(item["threadID"])
            if page >= data["pagination"]["totalPages"]:
                break
            page += 1

    for tid in thread_ids:
        thread = zmail("getThread", threadID=tid)
        for m in thread["items"]:
            found_ids.add(m["messageID"])

    missing = [mid for mid in found_ids if mid not in cached]
    for chunk_start in range(0, len(missing), 10):
        chunk = missing[chunk_start : chunk_start + 10]
        data = zmail("getMessages", ids=chunk)
        for msg in data["items"]:
            cached[msg["messageID"]] = msg
            (CACHE_DIR / f"msg_{msg['messageID']}.json").write_text(
                json.dumps(msg, ensure_ascii=False, indent=2)
            )

    return [cached[mid] for mid in found_ids if mid in cached]


def msg_sort_key(msg: dict) -> str:
    return msg.get("date") or ""


def extract_date(messages: list[dict]) -> str | None:
    # Latest security message that talks about an attack and contains a date.
    candidates = [
        m for m in messages
        if "security" in (m.get("from") or "")
        and any(kw in (m.get("message") or "").lower() for kw in ATTACK_KEYWORDS)
    ]
    candidates.sort(key=msg_sort_key, reverse=True)
    for msg in candidates:
        for match in DATE_IN_TEXT_RE.finditer(msg.get("message") or ""):
            return match.group(1)
    return None


def extract_confirmation_code(messages: list[dict]) -> str | None:
    # Walk newest-first so the corrected code wins over the original typo.
    sec_msgs = [
        m for m in messages
        if CONFIRMATION_IN_TEXT_RE.search(m.get("message") or "")
    ]
    sec_msgs.sort(key=msg_sort_key, reverse=True)
    for msg in sec_msgs:
        codes = CONFIRMATION_IN_TEXT_RE.findall(msg.get("message") or "")
        if codes:
            return codes[-1]
    return None


def extract_password(messages: list[dict]) -> str | None:
    # Match the password-rotation email from security; latest one wins.
    candidates = [
        m for m in messages
        if "security" in (m.get("from") or "")
        and "hasł" in (m.get("subject", "") + " " + (m.get("message") or "")).lower()
    ]
    candidates.sort(key=msg_sort_key, reverse=True)
    for msg in candidates:
        match = PASSWORD_LINE_RE.search(msg.get("message") or "")
        if match:
            return match.group(1).strip()
    return None


def extract_with_gemini(messages: list[dict]) -> dict[str, str | None]:
    from google import genai
    from google.genai import types
    from pydantic import BaseModel

    class Answer(BaseModel):
        date: str | None
        password: str | None
        confirmation_code: str | None

    rendered = [
        f"--- {msg['messageID']} | {msg.get('from')} | {msg.get('date')} | "
        f"{msg.get('subject')} ---\n{msg.get('message') or ''}"
        for msg in messages
    ]
    prompt = (
        "Z poniższych maili wyciągnij: date (YYYY-MM-DD planowanego ataku/"
        "bombardowania PWR6132PL), password (do systemu pracowniczego), "
        "confirmation_code (SEC- + 32 znaki — użyj POPRAWIONEJ wersji jeśli "
        "wystąpi korekta). Zwróć null dla brakujących pól.\n\n"
        + "\n\n".join(rendered)
    )
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-lite"),
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Answer,
        ),
    )
    return response.parsed.model_dump()


def build_answer(messages: list[dict]) -> dict[str, str | None]:
    answer = {
        "date": extract_date(messages),
        "password": extract_password(messages),
        "confirmation_code": extract_confirmation_code(messages),
    }
    missing = [k for k, v in answer.items() if v is None]
    if missing and os.environ.get("USE_GEMINI") == "1":
        print(f"regex missed {missing}; falling back to Gemini")
        gemini_answer = extract_with_gemini(messages)
        for k in missing:
            answer[k] = gemini_answer.get(k)
    return answer


def validate(answer: dict[str, str | None]) -> list[str]:
    issues = []
    if not answer.get("date") or not DATE_RE.match(answer["date"]):
        issues.append(f"date invalid: {answer.get('date')!r}")
    if not answer.get("password"):
        issues.append("password missing")
    code = answer.get("confirmation_code")
    if not code or not CONFIRMATION_RE.match(code):
        issues.append(f"confirmation_code invalid: {code!r}")
    return issues


def main() -> None:
    load_dotenv()

    print("Discovery: GET help")
    help_info = zmail("help")
    print(json.dumps(help_info, ensure_ascii=False, indent=2)[:600])

    for attempt in range(1, 6):
        print(f"\n=== attempt {attempt} ===")
        messages = collect_messages()
        print(f"collected {len(messages)} unique messages")

        answer = build_answer(messages)
        print(f"extracted: {answer}")

        issues = validate(answer)
        if issues:
            print(f"validation issues: {issues}; mailbox is live, retrying after 15s")
            time.sleep(15)
            continue

        print(f"submitting: {answer}")
        try:
            result = submit_answer("mailbox", answer)
        except requests.HTTPError as exc:
            body = exc.response.text if exc.response is not None else ""
            print(f"hub HTTP error: {exc}\n{body}")
            time.sleep(15)
            continue

        print(json.dumps(result, ensure_ascii=False, indent=2))
        if "FLG" in json.dumps(result, ensure_ascii=False):
            print("DONE")
            return
        print("hub rejected — retrying")
        time.sleep(15)

    print("exhausted attempts", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
