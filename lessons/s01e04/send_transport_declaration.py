"""Wypełnia i wysyła deklarację SPK do Centrali (task: sendit).

Pobiera dokumentację z hub.ag3nts.org, używa Gemini Vision do odczytania kodu
trasy z `trasy-wylaczone.png`, składa deklarację zgodnie ze wzorem z
`zalacznik-E.md` i wysyła ją do `/verify`.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import date
from pathlib import Path

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

from aidevs4.centrala import submit_answer

DOC_BASE = "https://hub.ag3nts.org/dane/doc"
CACHE_DIR = Path(__file__).parent / "cache"
MODEL = "gemini-2.5-flash"

DOCS_TO_FETCH = [
    "index.md",
    "zalacznik-E.md",
    "zalacznik-F.md",
    "zalacznik-G.md",
    "zalacznik-H.md",
    "dodatkowe-wagony.md",
    "trasy-wylaczone.png",
]


class RouteCode(BaseModel):
    code: str


def fetch_doc(filename: str) -> bytes:
    CACHE_DIR.mkdir(exist_ok=True)
    path = CACHE_DIR / filename
    if path.exists():
        return path.read_bytes()
    print(f"[fetch] {DOC_BASE}/{filename}")
    response = requests.get(f"{DOC_BASE}/{filename}", timeout=30)
    response.raise_for_status()
    path.write_bytes(response.content)
    return response.content


def extract_route_code(client: genai.Client, png: bytes) -> str:
    prompt = (
        "Na obrazku znajduje się tabela tras kolejowych wyłączonych z użytku w "
        "ramach Systemu Przesyłek Konduktorskich (SPK). Każda trasa ma kod w "
        "formacie typu 'X-NN' (np. X-01, X-12). Znajdź wiersz dotyczący "
        "połączenia GDAŃSK – ŻARNOWIEC i zwróć WYŁĄCZNIE kod tej trasy."
    )
    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=png, mime_type="image/png"),
            prompt,
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RouteCode,
        ),
    )
    parsed: RouteCode = response.parsed
    code = parsed.code.strip()
    if not re.match(r"^[A-Z]+-\d+$", code):
        raise ValueError(f"Vision returned invalid route code: {code!r}")
    return code


def build_declaration(route_code: str) -> str:
    return (
        "SYSTEM PRZESYŁEK KONDUKTORSKICH - DEKLARACJA ZAWARTOŚCI\n"
        "======================================================\n"
        f"DATA: {date.today().isoformat()}\n"
        "PUNKT NADAWCZY: Gdańsk\n"
        "------------------------------------------------------\n"
        "NADAWCA: 450202122\n"
        "PUNKT DOCELOWY: Żarnowiec\n"
        f"TRASA: {route_code}\n"
        "------------------------------------------------------\n"
        "KATEGORIA PRZESYŁKI: A\n"
        "------------------------------------------------------\n"
        "OPIS ZAWARTOŚCI (max 200 znaków): kasety z paliwem do reaktora\n"
        "------------------------------------------------------\n"
        "DEKLAROWANA MASA (kg): 2800\n"
        "------------------------------------------------------\n"
        "WDP: 4\n"
        "------------------------------------------------------\n"
        "UWAGI SPECJALNE: brak\n"
        "------------------------------------------------------\n"
        "KWOTA DO ZAPŁATY: 0 PP\n"
        "------------------------------------------------------\n"
        "OŚWIADCZAM, ŻE PODANE INFORMACJE SĄ PRAWDZIWE.\n"
        "BIORĘ NA SIEBIE KONSEKWENCJĘ ZA FAŁSZYWE OŚWIADCZENIE.\n"
        "======================================================"
    )


def main() -> None:
    load_dotenv()

    for filename in DOCS_TO_FETCH:
        fetch_doc(filename)
    png = (CACHE_DIR / "trasy-wylaczone.png").read_bytes()

    override = os.environ.get("ROUTE_CODE")
    if override:
        route_code = override.strip()
        print(f"[route] using override: {route_code}")
    else:
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        route_code = extract_route_code(client, png)
        print(f"[route] extracted from image: {route_code}")

    declaration = build_declaration(route_code)
    print("\n----- DEKLARACJA -----")
    print(declaration)
    print("----- /DEKLARACJA -----\n")

    print("Wysyłam do Centrali...")
    try:
        result = submit_answer("sendit", {"declaration": declaration})
    except requests.HTTPError as exc:
        print(f"HTTP error: {exc}")
        if exc.response is not None:
            print("Response body:", exc.response.text)
        sys.exit(1)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
