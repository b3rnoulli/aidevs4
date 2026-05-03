import csv
import json
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

from aidevs4.centrala import submit_answer

CSV_PATH = Path(__file__).parent / "people.csv"
TARGET_CITY = "Grudziądz"
MIN_BIRTH_YEAR = 1986  # age 40 in 2026
MAX_BIRTH_YEAR = 2006  # age 20 in 2026
MODEL = "gemini-2.5-flash"

Tag = Literal[
    "IT",
    "transport",
    "edukacja",
    "medycyna",
    "praca z ludźmi",
    "praca z pojazdami",
    "praca fizyczna",
]

TAG_DESCRIPTIONS = {
    "IT": "informatyka, programowanie, administracja systemami, dane, oprogramowanie",
    "transport": "przewóz osób lub towarów, logistyka, spedycja, kierowca zawodowy, kolej, lotnictwo, żegluga",
    "edukacja": "nauczanie, szkolenia, prowadzenie zajęć, praca w szkole/uczelni",
    "medycyna": "ochrona zdrowia, leczenie, opieka nad pacjentem, farmacja",
    "praca z ludźmi": "obsługa klienta, doradztwo, sprzedaż, kontakt interpersonalny jako rdzeń pracy",
    "praca z pojazdami": "naprawa, serwis, mechanika lub obsługa techniczna pojazdów (niekoniecznie ich prowadzenie)",
    "praca fizyczna": "praca wymagająca wysiłku fizycznego, manualna, na budowie, w produkcji",
}


class TaggedJob(BaseModel):
    index: int
    tags: list[Tag]


def load_candidates() -> list[dict]:
    candidates = []
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["gender"] != "M":
                continue
            if row["birthPlace"] != TARGET_CITY:
                continue
            year = int(row["birthDate"].split("-")[0])
            if not (MIN_BIRTH_YEAR <= year <= MAX_BIRTH_YEAR):
                continue
            row["_year"] = year
            candidates.append(row)
    return candidates


def tag_jobs(client: genai.Client, candidates: list[dict]) -> list[TaggedJob]:
    descriptions = "\n".join(f"- {tag}: {desc}" for tag, desc in TAG_DESCRIPTIONS.items())
    numbered_jobs = "\n".join(f"{i}. {c['job']}" for i, c in enumerate(candidates))

    prompt = (
        "Otrzymujesz ponumerowaną listę opisów stanowisk pracy. "
        "Dla każdego rekordu przypisz jeden lub więcej tagów z poniższej listy. "
        "Tagi i ich znaczenie:\n"
        f"{descriptions}\n\n"
        "Zwróć listę obiektów {index, tags}, po jednym dla KAŻDEGO rekordu. "
        "Używaj wyłącznie tagów z listy powyżej.\n\n"
        "Rekordy:\n"
        f"{numbered_jobs}"
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[TaggedJob],
        ),
    )
    return response.parsed


def main() -> None:
    load_dotenv()
    candidates = load_candidates()
    print(f"After demographic filter: {len(candidates)} candidates")
    for c in candidates:
        print(f"  - {c['name']} {c['surname']} ({c['_year']}): {c['job'][:80]}...")

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    tagged = tag_jobs(client, candidates)

    by_index = {t.index: t.tags for t in tagged}
    transport_people = [
        c for i, c in enumerate(candidates)
        if "transport" in by_index.get(i, [])
    ]
    print(f"\nAfter transport-tag filter: {len(transport_people)} people")

    answer = [
        {
            "name": c["name"],
            "surname": c["surname"],
            "gender": c["gender"],
            "born": c["_year"],
            "city": c["birthPlace"],
            "tags": by_index[i],
        }
        for i, c in enumerate(candidates)
        if "transport" in by_index.get(i, [])
    ]
    print(json.dumps(answer, ensure_ascii=False, indent=2))

    print("\nSubmitting to Centrala...")
    result = submit_answer("people", answer)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
