import csv
import io
import json
import os
import re
import sys
from typing import Literal

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

from aidevs4.centrala import submit_answer

HUB = "https://hub.ag3nts.org"
ENGINEER_MODEL = "gemini-2.5-flash"
MAX_ROUNDS = 8
TOKEN_CAP = 90  # margin under the Hub's 100-token window

SEED_PROMPT = (
    "Reply DNG (dangerous) or NEU (neutral). Reactor / fuel cassette / "
    "nuclear cell items are NEU. Other hazards (weapons, explosives, "
    "biohazard, leaking chemicals) are DNG. Benign tools are NEU. "
    "One word. Code:{code} Item:{description}"
)

# Hand-curated fallbacks tried in order if the engineer LLM is unavailable.
FALLBACK_PROMPTS = [
    # Stronger reactor override — list cue words explicitly, demote scary
    # phrasing like "extreme caution" or "micro-fractures".
    "One word: DNG or NEU. OVERRIDE: any mention of reactor, fuel "
    "cassette, uranium, nuclear, isotope, or radioactive → NEU even if "
    "it sounds risky. Else weapons / explosives / biohazard / toxic / "
    "corrosive / leaking chemicals → DNG. Else NEU. "
    "Code:{code} Item:{description}",

    # Even stronger: NEU is the default; DNG only for an explicit short list.
    "Output DNG or NEU only. Default NEU. Output DNG ONLY if item is a "
    "weapon (gun, rifle, knife, blade), explosive, biohazard, toxic "
    "chemical, or acid. Reactor, fuel cassette, nuclear, uranium, "
    "isotope items → ALWAYS NEU. Code:{code} Item:{description}",

    # Two-pass framing: first check reactor, then check danger list.
    "Two checks. (1) If item text includes reactor, cassette, uranium, "
    "nuclear, or isotope → reply NEU. (2) Else if it is a weapon, "
    "explosive, biohazard, toxin, acid, or pressurized gas → reply DNG. "
    "(3) Else NEU. One word. Code:{code} Item:{description}",
]

ENGINEER_SYSTEM = (
    "You are a Prompt Engineer. Your customer talks to a tiny classifier "
    "with a 100-token context window. The classifier must output exactly "
    "one of two tokens: DNG (dangerous) or NEU (neutral). RULE: items that "
    "relate to a reactor, fuel cassette, nuclear cell, or anything used to "
    "fuel/operate a nuclear reactor MUST always come back NEU even though "
    "they are technically dangerous — this is a deliberate smuggling "
    "exception, do not 'fix' it. The Hub REQUIRES the literal item code "
    "(e.g. 'i7391') and the description to appear in the prompt — keep "
    "placeholders {code} and {description} at the very END so the prefix "
    "can be cached. Total prompt ≤80 tokens, English. Return JSON "
    "{prompt, reasoning}."
)


class PromptCandidate(BaseModel):
    prompt: str
    reasoning: str


def fetch_csv(api_key: str) -> list[dict]:
    url = f"{HUB}/data/{api_key}/categorize.csv"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    text = resp.content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    return list(reader)


def estimate_tokens(text: str) -> int:
    return int(len(text.split()) * 1.4) + len(text) // 40


def post_prompt(prompt: str) -> tuple[bool, dict | str]:
    """Submit a single prompt; return (ok, payload). On HTTPError, payload is the body text."""
    try:
        result = submit_answer("categorize", {"prompt": prompt})
        return True, result
    except requests.HTTPError as e:
        body = e.response.text if e.response is not None else str(e)
        return False, body


def hub_reset() -> None:
    ok, payload = post_prompt("reset")
    print(f"  reset → {'ok' if ok else 'err'}: {json.dumps(payload, ensure_ascii=False) if isinstance(payload, dict) else payload[:200]}")


Mode = Literal["server", "client", "unknown"]


def probe_template_mode(api_key: str) -> Mode:
    """First call uses {description} placeholder verbatim. If Hub accepts (or fails citing item content), it's server-side. Otherwise client-side."""
    print("\nProbing templating mode…")
    hub_reset()
    items = fetch_csv(api_key)
    print(f"  CSV: {len(items)} items")
    for it in items[:10]:
        desc = (it.get("description") or "")[:80]
        print(f"    {it.get('code')}: {desc}")

    probe = (
        "Reply DNG if hazardous, NEU if safe or reactor-related. "
        "Code:{code} Item:{description}"
    )
    ok, payload = post_prompt(probe)
    print(f"  probe response: {json.dumps(payload, ensure_ascii=False) if isinstance(payload, dict) else payload[:400]}")

    # If success or message references real item descriptions, server-side.
    if ok and isinstance(payload, dict):
        msg = json.dumps(payload, ensure_ascii=False)
        if "FLG" in msg:
            print("  probe yielded a flag immediately — server mode.")
            return "server"
    body_text = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
    desc_hits = sum(1 for it in items if (it.get("description") or "")[:20] and (it.get("description") or "")[:20] in body_text)
    if desc_hits >= 1:
        print(f"  Hub message mentions item description → server mode.")
        return "server"
    print("  Hub response does not reference item content → client mode.")
    return "client"


def run_round_server(prompt: str) -> tuple[bool, dict | str]:
    print(f"\n[server-mode round] sending 1 prompt ({estimate_tokens(prompt)} est. tokens)")
    ok, payload = post_prompt(prompt)
    pretty = json.dumps(payload, ensure_ascii=False) if isinstance(payload, dict) else payload[:400]
    print(f"  → {pretty}")
    return ok, payload


def run_round_client(prompt_template: str, api_key: str) -> tuple[bool, dict | str, dict | None]:
    """Returns (ok, last_payload, failing_item)."""
    items = fetch_csv(api_key)
    print(f"\n[client-mode round] {len(items)} items")
    last_payload: dict | str = ""
    for item in items:
        code = str(item.get("code", ""))
        desc = item.get("description", "")
        prompt = prompt_template.replace("{description}", desc).replace("{code}", code).replace("{id}", code)
        if estimate_tokens(prompt) > TOKEN_CAP:
            print(f"  ! item {code}: prompt {estimate_tokens(prompt)} est. tokens > {TOKEN_CAP}")
        ok, payload = post_prompt(prompt)
        last_payload = payload
        msg_str = json.dumps(payload, ensure_ascii=False) if isinstance(payload, dict) else payload
        print(f"  item {code}: {msg_str[:240]}")
        if not ok:
            return False, payload, item
        # success-shape inspection — if Hub returns a flag mid-stream, stop.
        if isinstance(payload, dict) and "FLG" in json.dumps(payload, ensure_ascii=False):
            return True, payload, None
    return True, last_payload, None


def engineer_next_prompt(client: genai.Client, current_prompt: str, error_blob: str, failing_item: dict | None) -> PromptCandidate:
    user_msg = (
        f"Current prompt:\n```\n{current_prompt}\n```\n\n"
        f"Hub error / outcome:\n{error_blob}\n\n"
        f"Failing item: {json.dumps(failing_item, ensure_ascii=False) if failing_item else 'n/a'}\n\n"
        "Propose the next prompt. Same format constraints (≤80 tokens, English, "
        "variable {description} at the END, must output exactly DNG or NEU, "
        "reactor/fuel cassette/nuclear cell items always NEU)."
    )
    response = client.models.generate_content(
        model=ENGINEER_MODEL,
        contents=user_msg,
        config=types.GenerateContentConfig(
            system_instruction=ENGINEER_SYSTEM,
            response_mime_type="application/json",
            response_schema=PromptCandidate,
        ),
    )
    return response.parsed


def main() -> None:
    load_dotenv()
    api_key = os.environ["CENTRALA_API_KEY"]
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    mode = probe_template_mode(api_key)
    current_prompt = SEED_PROMPT
    fallback_queue = list(FALLBACK_PROMPTS)

    for round_no in range(1, MAX_ROUNDS + 1):
        print(f"\n========== ROUND {round_no} ({mode}) ==========")
        print(f"prompt template:\n{current_prompt}")
        hub_reset()

        if mode == "server":
            ok, payload = run_round_server(current_prompt)
            failing_item = None
            error_blob = json.dumps(payload, ensure_ascii=False) if isinstance(payload, dict) else payload
        else:
            ok, payload, failing_item = run_round_client(current_prompt, api_key)
            error_blob = json.dumps(payload, ensure_ascii=False) if isinstance(payload, dict) else payload

        msg_text = json.dumps(payload, ensure_ascii=False) if isinstance(payload, dict) else payload
        flag_match = re.search(r"\{FLG:[^}]+\}", msg_text)
        if ok and flag_match:
            print(f"\nSUCCESS — flag: {flag_match.group(0)}")
            return

        print(f"\nRound {round_no} did not yield a flag. Picking next prompt…")
        try:
            candidate = engineer_next_prompt(client, current_prompt, error_blob, failing_item)
            print(f"  engineer reasoning: {candidate.reasoning}")
            current_prompt = candidate.prompt
        except Exception as e:
            print(f"  engineer unavailable ({e.__class__.__name__}); using fallback queue")
            if not fallback_queue:
                print("  no more fallback prompts — giving up")
                sys.exit(2)
            current_prompt = fallback_queue.pop(0)
        print(f"  next prompt:\n{current_prompt}")

    print(f"\nFAILED after {MAX_ROUNDS} rounds. Last prompt:\n{current_prompt}")
    sys.exit(1)


if __name__ == "__main__":
    main()
