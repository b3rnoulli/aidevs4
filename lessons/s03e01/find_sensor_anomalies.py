import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors
from google.genai import types
from pydantic import BaseModel

from aidevs4.centrala import submit_answer

SENSORS_DIR = Path(__file__).parent / "sensors"
MODEL = "gemini-flash-latest"
NOTES_PER_BATCH = 250
MAX_BATCH_RETRIES = 5

# sensor name in `sensor_type` → measurement field, valid range
SENSOR_SPEC: dict[str, tuple[str, float, float]] = {
    "temperature": ("temperature_K",       553.0, 873.0),
    "pressure":    ("pressure_bar",         60.0, 160.0),
    "water":       ("water_level_meters",    5.0,  15.0),
    "voltage":     ("voltage_supply_v",    229.0, 231.0),
    "humidity":    ("humidity_percent",     40.0,  80.0),
}
ALL_FIELDS = [spec[0] for spec in SENSOR_SPEC.values()]


def file_id(path: Path) -> str:
    return path.stem  # "0001"


def is_data_anomalous(record: dict) -> bool:
    active = [s for s in record["sensor_type"].split("/") if s]
    active_fields = set()
    for sensor in active:
        field, lo, hi = SENSOR_SPEC[sensor]
        active_fields.add(field)
        value = record.get(field, 0)
        if not (lo <= value <= hi):
            return True
    for field in ALL_FIELDS:
        if field in active_fields:
            continue
        if record.get(field, 0) != 0:
            return True
    return False


class NoteClassification(BaseModel):
    index: int
    claims_issue: bool


def _classify_batch(client: genai.Client, batch: list[str]) -> list[NoteClassification]:
    numbered = "\n".join(f"{i}. {n}" for i, n in enumerate(batch))
    prompt = (
        "Otrzymujesz ponumerowane notatki operatora elektrowni po angielsku. "
        "Dla każdej notatki zdecyduj, czy operator sygnalizuje problem ze "
        "sprzętem / odczytami / czujnikami (claims_issue=true), "
        "czy raportuje brak problemu / wszystko w normie / rutynowy odczyt "
        "(claims_issue=false). Niejasne lub neutralne notatki traktuj jako "
        "claims_issue=false. Zwróć dokładnie po jednym obiekcie "
        "{index, claims_issue} dla KAŻDEJ notatki.\n\n"
        f"Notatki:\n{numbered}"
    )
    for attempt in range(MAX_BATCH_RETRIES):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=list[NoteClassification],
                ),
            )
            return response.parsed or []
        except genai_errors.ServerError as e:
            wait = 2 ** attempt
            print(f"    server error (attempt {attempt+1}): {str(e)[:80]} — sleeping {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"Gemini failed for batch after {MAX_BATCH_RETRIES} retries")


def classify_notes(client: genai.Client, notes: list[str]) -> dict[str, bool]:
    """Return note → True if operator note implies sensors/data have a problem."""
    if not notes:
        return {}
    result: dict[str, bool] = {}
    for start in range(0, len(notes), NOTES_PER_BATCH):
        batch = notes[start : start + NOTES_PER_BATCH]
        print(f"  classifying notes {start}..{start + len(batch) - 1} ({len(batch)})")
        parsed = _classify_batch(client, batch)
        for item in parsed:
            if 0 <= item.index < len(batch):
                result[batch[item.index]] = item.claims_issue
        missing = [n for n in batch if n not in result]
        if missing:
            print(f"    !! batch returned no classification for {len(missing)} notes; defaulting to False")
            for n in missing:
                result.setdefault(n, False)
    return result


def main() -> None:
    load_dotenv()
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    files = sorted(SENSORS_DIR.glob("*.json"))
    print(f"Loaded {len(files)} sensor files")

    data_bad: set[str] = set()
    note_to_files: dict[str, list[str]] = {}
    for path in files:
        record = json.loads(path.read_text(encoding="utf-8"))
        fid = file_id(path)
        if is_data_anomalous(record):
            data_bad.add(fid)
            continue
        note_to_files.setdefault(record["operator_notes"], []).append(fid)

    print(f"  programmatic anomalies: {len(data_bad)}")
    print(f"  remaining files (data OK): {sum(len(v) for v in note_to_files.values())}")
    print(f"  unique operator notes among them: {len(note_to_files)}")

    note_flags = classify_notes(client, list(note_to_files.keys()))
    note_bad: set[str] = set()
    for note, claims_issue in note_flags.items():
        if claims_issue:
            note_bad.update(note_to_files[note])
    print(f"  notes flagged 'claims_issue': {sum(1 for v in note_flags.values() if v)}")
    print(f"  files flagged via note: {len(note_bad)}")

    flagged = sorted(data_bad | note_bad, key=int)
    print(f"\ntotal anomalies: {len(flagged)}")
    print(f"first 20: {flagged[:20]}")

    print("\nSubmitting to Centrala…")
    result = submit_answer("evaluation", {"recheck": flagged})
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
