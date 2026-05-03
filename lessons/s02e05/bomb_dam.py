"""Solve task 'drone': bomb the dam (not the plant) by feeding the docs and a
vision-derived dam location into Gemini, then iterating on the /verify endpoint.

The drone manifest must list power plant PWR6132PL as the official target, but
the bomb has to fall on the nearby dam so its water reaches the plant cooling
system. We feed the API docs and dam coordinates to Gemini, post the resulting
instructions to /verify, and re-prompt with the error body until the response
contains a {FLG:...} marker.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors
from google.genai import types
from pydantic import BaseModel, Field

from aidevs4.centrala import submit_answer

TASK = "drone"
PLANT_CODE = "PWR6132PL"
DOCS_URL = "https://hub.ag3nts.org/dane/drone.html"
MAP_URL_TMPL = "https://hub.ag3nts.org/data/{key}/drone.png"
PRIMARY_MODEL = "gemini-2.5-flash"
FALLBACK_MODELS = ("gemini-2.5-flash-lite", "gemini-2.0-flash")
MAX_ITERATIONS_DEFAULT = 8
LESSON_DIR = Path(__file__).parent
MAP_PATH = LESSON_DIR / "drone.png"
DOCS_PATH = LESSON_DIR / "drone.html"
FLAG_RE = re.compile(r"\{FLG:[^}]+\}")


class GridLocation(BaseModel):
    columns: int = Field(description="Total grid columns visible on the map.")
    rows: int = Field(description="Total grid rows visible on the map.")
    dam_column: int = Field(description="1-indexed column of the dam sector.")
    dam_row: int = Field(description="1-indexed row of the dam sector.")
    reasoning: str = Field(
        description="Brief explanation of how the dam sector was identified."
    )


class DroneInstructions(BaseModel):
    instructions: list[str] = Field(
        description="Ordered list of textual drone commands."
    )
    rationale: str = Field(
        description="Why this command sequence accomplishes the mission."
    )


def _load_env() -> None:
    """Load .env from worktree or main-repo location."""
    here = Path(__file__).resolve()
    candidates = [here.parents[2] / ".env", here.parents[5] / ".env"]
    for path in candidates:
        if path.exists():
            load_dotenv(path)
    for var in ("CENTRALA_API_KEY", "GEMINI_API_KEY"):
        if not os.environ.get(var):
            print(f"{var} missing from environment", file=sys.stderr)
            sys.exit(2)


def _download_once(url: str, dest: Path, *, expect_image: bool = False) -> bytes:
    if dest.exists():
        return dest.read_bytes()
    print(f"[fetch] {url} -> {dest.name}")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    if expect_image:
        ctype = response.headers.get("content-type", "")
        if not ctype.startswith("image/"):
            raise RuntimeError(
                f"Expected image content-type from {url}, got {ctype!r}; "
                f"body starts: {response.text[:120]!r}"
            )
    dest.write_bytes(response.content)
    return response.content


def _generate_with_fallback(
    client: genai.Client,
    contents: list,
    config: types.GenerateContentConfig,
):
    """Try primary model; fall back to lighter models on quota errors."""
    last_exc: Exception | None = None
    for model in (PRIMARY_MODEL, *FALLBACK_MODELS):
        for attempt in range(3):
            try:
                return client.models.generate_content(
                    model=model, contents=contents, config=config
                )
            except genai_errors.ClientError as exc:
                last_exc = exc
                if exc.code == 429:
                    wait = 5.0 * (attempt + 1)
                    print(
                        f"[gemini] {model} 429 (attempt {attempt + 1}); "
                        f"sleeping {wait:.0f}s",
                        file=sys.stderr,
                    )
                    time.sleep(wait)
                    continue
                raise
        print(f"[gemini] {model} exhausted retries; trying next model", file=sys.stderr)
    raise RuntimeError(f"All Gemini models rate-limited: {last_exc}")


def extract_dam_location(client: genai.Client, png: bytes) -> GridLocation:
    prompt = (
        "Analizujesz mapę poglądową terenu elektrowni jądrowej w Żarnowcu. "
        "Mapa jest podzielona równą siatką na sektory. W pobliżu elektrowni "
        "znajduje się tama (zapora wodna), która przy mapowaniu została "
        "celowo wyróżniona przez podbicie intensywności koloru wody (woda jest "
        "wyraźnie bardziej nasycona/jaskrawa niż naturalna).\n\n"
        "Zadania:\n"
        "1. Policz dokładnie liczbę kolumn (columns) i wierszy (rows) widocznej siatki.\n"
        "2. Zlokalizuj sektor zawierający tamę.\n"
        "3. Indeksuj od 1: kolumna 1 = lewa krawędź, wiersz 1 = górna krawędź.\n"
        "4. Wyjaśnij krótko, po czym rozpoznałeś tamę (kolor wody, kontekst).\n\n"
        "Zwróć JSON zgodny ze schematem GridLocation."
    )
    response = _generate_with_fallback(
        client,
        contents=[types.Part.from_bytes(data=png, mime_type="image/png"), prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=GridLocation,
            temperature=0.0,
        ),
    )
    parsed: GridLocation = response.parsed
    if not (1 <= parsed.dam_column <= parsed.columns):
        raise ValueError(
            f"dam_column {parsed.dam_column} outside 1..{parsed.columns}"
        )
    if not (1 <= parsed.dam_row <= parsed.rows):
        raise ValueError(f"dam_row {parsed.dam_row} outside 1..{parsed.rows}")
    return parsed


def generate_instructions(
    client: genai.Client,
    docs_html: str,
    dam_col: int,
    dam_row: int,
    grid_columns: int,
    grid_rows: int,
    history: list[dict],
) -> DroneInstructions:
    history_text = (
        "Brak wcześniejszych prób — pierwsza iteracja."
        if not history
        else "\n\n".join(
            f"PRÓBA {h['attempt']}\n"
            f"WYSŁANE INSTRUKCJE: {json.dumps(h['instructions'], ensure_ascii=False)}\n"
            f"ODPOWIEDŹ SERWERA: {json.dumps(h['response'], ensure_ascii=False)}"
            for h in history
        )
    )
    prompt = f"""Jesteś projektantem misji uzbrojonego drona. Twoje zadanie:
przygotować listę instrukcji (pole `instructions`) wysyłanych do API drona,
zgodnie z dokumentacją poniżej, tak aby:

- Manifest misji oficjalnie wskazywał elektrownię o kodzie `{PLANT_CODE}`
  jako cel zniszczenia.
- Bomba **w rzeczywistości** spadła na sektor TAMY w siatce mapy:
  kolumna={dam_col}, wiersz={dam_row} (indeksowanie od 1, kolumna 1 = lewa,
  wiersz 1 = góra). Cała siatka mapy ma {grid_columns} kolumn i {grid_rows} wierszy.

WAŻNE ZASADY:
1. Czytaj dokumentację KRYTYCZNIE — zawiera celowe pułapki, sprzeczne nazwy
   funkcji oraz funkcje, które zachowują się różnie w zależności od parametrów.
   Wybierz tylko te, które są niezbędne do wykonania misji. Oszczędzaj tokeny.
2. Funkcja `hardReset` (jeśli występuje w dokumentacji) jest dostępna na wypadek
   skumulowanych błędów konfiguracyjnych. Rozważ jej użycie na początku
   sekwencji, jeśli to bezpieczne i sensowne.
3. Mapa używa układu (kolumna, wiersz) indeksowanego od 1. API drona może
   używać innego układu (np. (x,y), (lat,lng), 0-indexed). Przetłumacz
   współrzędne na układ wymagany przez API zgodnie z dokumentacją.
4. Język instrukcji wysyłanych do API powinien odpowiadać formatowi widocznemu
   w dokumentacji (Polski, angielski, wywołania funkcji itp.).
5. Zwracaj wyłącznie JSON zgodny ze schematem DroneInstructions
   (`instructions: list[str]` + `rationale: str`).

DOKUMENTACJA API DRONA (HTML):
\"\"\"
{docs_html}
\"\"\"

HISTORIA POPRZEDNICH PRÓB I ODPOWIEDZI SERWERA:
{history_text}

Jeśli historia zawiera komunikaty błędów — przeanalizuj je dokładnie i skoryguj
listę instrukcji. Każdy błąd zawiera precyzyjną wskazówkę co poprawić.
Sukces sygnalizowany jest przez `{{FLG:...}}` w odpowiedzi.

Zwróć JSON: {{"instructions": [...], "rationale": "..."}}.
"""
    response = _generate_with_fallback(
        client,
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=DroneInstructions,
            temperature=0.2,
        ),
    )
    return response.parsed


def submit(instructions: list[str]) -> dict:
    try:
        return submit_answer(TASK, {"instructions": instructions})
    except requests.HTTPError as exc:
        if exc.response is not None:
            try:
                return exc.response.json()
            except ValueError:
                return {"error": exc.response.text, "status": exc.response.status_code}
        return {"error": str(exc)}


def find_flag(response: dict) -> str | None:
    match = FLAG_RE.search(json.dumps(response, ensure_ascii=False))
    return match.group(0) if match else None


def _baseline_instructions(col: int, row: int) -> list[str]:
    """Hardcoded sequence derived from drone.html — used as Gemini fallback.

    Manifest target = the plant (PWR6132PL); landing sector = the dam (col, row)
    on the plant's perimeter map.
    """
    return [
        "hardReset",
        f"setDestinationObject({PLANT_CODE})",
        f"set({col},{row})",
        "set(50m)",
        "set(engineON)",
        "set(60%)",
        "set(destroy)",
        "set(return)",
        "calibrateCompass",
        "calibrateGPS",
        "selfCheck",
        "flyToLocation",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Solve s02e05 drone task.")
    parser.add_argument(
        "--manual-coords",
        metavar="COL,ROW",
        help="Skip vision step; force dam location, e.g. 2,4",
    )
    parser.add_argument(
        "--grid",
        metavar="COLS,ROWS",
        default="3,4",
        help="Total grid dimensions (columns,rows) — used only with --manual-coords.",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=MAX_ITERATIONS_DEFAULT,
        help=f"Maximum reactive loop iterations (default {MAX_ITERATIONS_DEFAULT}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compose first attempt and print it, but do not POST.",
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Skip Gemini entirely; submit a hardcoded baseline derived from drone.html.",
    )
    args = parser.parse_args()

    _load_env()
    api_key = os.environ["CENTRALA_API_KEY"]
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    map_url = MAP_URL_TMPL.format(key=api_key)
    docs_html = _download_once(DOCS_URL, DOCS_PATH).decode("utf-8", errors="replace")
    png = _download_once(map_url, MAP_PATH, expect_image=True)

    if args.manual_coords:
        col, row = map(int, args.manual_coords.split(","))
        grid_columns, grid_rows = map(int, args.grid.split(","))
        print(
            f"[coords] manual override: dam @ col={col}, row={row} "
            f"(grid {grid_columns}x{grid_rows})"
        )
    else:
        loc = extract_dam_location(client, png)
        col, row = loc.dam_column, loc.dam_row
        grid_columns, grid_rows = loc.columns, loc.rows
        print(
            f"[coords] vision: grid {loc.columns}x{loc.rows}, "
            f"dam @ col={loc.dam_column}, row={loc.dam_row}"
        )
        print(f"[coords] reasoning: {loc.reasoning}")

    if args.no_llm:
        instructions = _baseline_instructions(col, row)
        print(
            f"[no-llm] baseline instructions: "
            f"{json.dumps(instructions, ensure_ascii=False, indent=2)}"
        )
        if args.dry_run:
            print("[dry-run] not submitting")
            return 0
        response = submit(instructions)
        print(json.dumps(response, ensure_ascii=False, indent=2))
        flag = find_flag(response)
        if flag:
            print(f"\nFLAG: {flag}")
            return 0
        return 1

    history: list[dict] = []
    for attempt in range(args.max_iterations):
        print(f"\n===== ATTEMPT {attempt} =====")
        gen = generate_instructions(
            client, docs_html, col, row, grid_columns, grid_rows, history
        )
        print(f"[try {attempt}] rationale: {gen.rationale}")
        print(
            f"[try {attempt}] instructions: "
            f"{json.dumps(gen.instructions, ensure_ascii=False, indent=2)}"
        )

        if args.dry_run and attempt == 0:
            print("[dry-run] not submitting")
            return 0

        response = submit(gen.instructions)
        print(
            f"[try {attempt}] response: "
            f"{json.dumps(response, ensure_ascii=False, indent=2)}"
        )

        history.append(
            {"attempt": attempt, "instructions": gen.instructions, "response": response}
        )

        flag = find_flag(response)
        if flag:
            print(f"\nFLAG: {flag}")
            return 0

    print("\nExhausted iterations without a flag.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
