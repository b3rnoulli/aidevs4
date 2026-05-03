import base64
import json
import os
import re
import time
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors
from google.genai import types
from pydantic import BaseModel

from aidevs4.centrala import submit_answer

TASK = "radiomonitoring"
DUMP_DIR = Path(__file__).parent / "captures"
MODEL = "gemini-flash-latest"
MAX_LISTEN = 80  # safety cap
MAX_LLM_RETRIES = 4


def listen_loop() -> list[dict]:
    DUMP_DIR.mkdir(exist_ok=True)
    print("→ start")
    print(json.dumps(submit_answer(TASK, {"action": "start"}), ensure_ascii=False))

    captures: list[dict] = []
    for i in range(1, MAX_LISTEN + 1):
        resp = submit_answer(TASK, {"action": "listen"})
        msg = resp.get("message", "")
        # heuristic: spec says system signals when material is exhausted.
        if resp.get("code") not in (100,):
            print(f"  listen #{i}: stop signal — code={resp.get('code')} message={msg!r}")
            print(json.dumps(resp, ensure_ascii=False, indent=2)[:1000])
            break
        if "transcription" in resp:
            t = resp["transcription"]
            captures.append({"i": i, "kind": "transcription", "text": t})
            print(f"  listen #{i}: transcription ({len(t)} chars)")
        elif "attachment" in resp:
            meta = resp.get("meta", "?")
            raw_b64 = resp["attachment"]
            data = base64.b64decode(raw_b64)
            (DUMP_DIR / f"chunk_{i:03d}.bin").write_bytes(data)
            captures.append({
                "i": i, "kind": "attachment", "meta": meta,
                "filesize": resp.get("filesize", len(data)),
                "data": data,
            })
            print(f"  listen #{i}: attachment meta={meta} bytes={len(data)}")
        else:
            print(f"  listen #{i}: unknown payload: {json.dumps(resp, ensure_ascii=False)[:300]}")
            captures.append({"i": i, "kind": "unknown", "raw": resp})
    return captures


TEXT_METAS = {"text/plain", "text/csv", "text/xml", "text/html", "application/json", "application/xml"}
MULTIMODAL_METAS = {"image/png", "image/jpeg", "image/webp", "audio/mpeg", "audio/wav", "audio/ogg", "audio/mp3"}


def render_capture(cap: dict) -> Optional[str]:
    """Turn one capture into text material the LLM can read; return None to defer to multimodal pass."""
    if cap["kind"] == "transcription":
        return cap["text"]
    if cap["kind"] == "attachment":
        meta = cap.get("meta", "")
        data = cap["data"]
        if meta in TEXT_METAS or meta.startswith("text/"):
            try:
                return data.decode("utf-8")
            except UnicodeDecodeError:
                return data.decode("utf-8", errors="replace")
        # Multimodal payloads handled separately.
        print(f"    [defer multimodal] capture #{cap['i']} meta={meta} size={len(data)}")
        return None
    return None


def build_aggregate(captures: list[dict]) -> str:
    sections = []
    for cap in captures:
        rendered = render_capture(cap)
        if not rendered:
            continue
        kind = cap["kind"]
        meta = cap.get("meta", "transcription")
        sections.append(f"--- chunk #{cap['i']} ({kind}, {meta}) ---\n{rendered}")
    return "\n\n".join(sections)


class ZionReport(BaseModel):
    cityName: str
    cityArea: float
    warehousesCount: int
    phoneNumber: str
    reasoning: str


def extract_report(client: genai.Client, aggregate: str, multimodal: list[dict]) -> ZionReport:
    instruction = (
        "Otrzymujesz transkrypcje rozmów radiowych, załączniki tekstowe oraz "
        "multimedialne (obrazy, audio) z nasłuchu radiowego. W eterze pojawia "
        "się miasto o kryptonimie **Syjon** (zwane też 'miastem ocalałych'). "
        "Odnajdź:\n"
        "- cityName — prawdziwa nazwa miasta nazywanego Syjonem,\n"
        "- cityArea — powierzchnia tego miasta (liczba),\n"
        "- warehousesCount — liczba magazynów aktualnie istniejących w Syjonie. "
        "Uwaga: jeśli ktoś mówi, że PLANUJĄ wybudować N-ty magazyn, to znaczy, "
        "że obecnie jest ich N-1.\n"
        "- phoneNumber — numer telefonu osoby kontaktowej z Syjonu, podawany "
        "wyłącznie jako ciąg cyfr (bez myślników i spacji).\n\n"
        "Wiele chunków to plotki/szum — ignoruj je. Pole reasoning wypełnij "
        "krótkim wyjaśnieniem, w których chunkach znalazłeś każdy fragment.\n\n"
        "Materiał tekstowy:\n"
        f"{aggregate}\n\n"
        "Załączniki multimedialne (kolejne części tej wiadomości):"
    )
    parts: list[types.Part] = [types.Part.from_text(text=instruction)]
    for cap in multimodal:
        parts.append(types.Part.from_text(text=f"\n[chunk #{cap['i']}, {cap['meta']}, {len(cap['data'])} bajtów]"))
        parts.append(types.Part.from_bytes(data=cap["data"], mime_type=cap["meta"]))

    last_err = None
    for attempt in range(MAX_LLM_RETRIES):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=parts,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ZionReport,
                ),
            )
            return response.parsed
        except genai_errors.ServerError as e:
            wait = 2 ** attempt
            last_err = e
            print(f"  Gemini server error attempt {attempt+1}: {str(e)[:80]}; sleeping {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"Gemini extraction failed: {last_err}")


def round2(area_value) -> str:
    """Format with exactly 2 decimal places (mathematical rounding)."""
    n = float(area_value)
    return f"{n + 1e-12:.2f}" if n >= 0 else f"{n:.2f}"


def main() -> None:
    load_dotenv()
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    captures = listen_loop()
    print(f"\n=== captured {len(captures)} chunks ===")

    aggregate = build_aggregate(captures)
    aggregate_path = DUMP_DIR / "aggregate.txt"
    aggregate_path.write_text(aggregate, encoding="utf-8")
    print(f"  aggregate text written to {aggregate_path} ({len(aggregate)} chars)")

    multimodal = [
        cap for cap in captures
        if cap["kind"] == "attachment" and cap.get("meta", "") in MULTIMODAL_METAS
    ]
    print(f"  multimodal chunks for Gemini: {[c['i'] for c in multimodal]}")

    report = extract_report(client, aggregate, multimodal)
    print("\n=== Extracted report ===")
    print(json.dumps(report.model_dump(), ensure_ascii=False, indent=2))

    answer = {
        "action": "transmit",
        "cityName": report.cityName,
        "cityArea": round2(report.cityArea),
        "warehousesCount": report.warehousesCount,
        "phoneNumber": report.phoneNumber,
    }
    print(f"\n→ transmit: {json.dumps(answer, ensure_ascii=False)}")
    result = submit_answer(TASK, answer)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
