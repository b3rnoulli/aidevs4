"""Build the virtual filesystem for the `filesystem` task.

Reads Natan's notes (ogloszenia.txt, rozmowy.txt, transakcje.txt) and
constructs three directories on the centrala virtual filesystem:

  /miasta/<city>  — JSON of items the city needs (qty without units)
  /osoby/<name>   — first+last name + markdown link to the city the person manages
  /towary/<item>  — markdown links to cities offering that item

Filename rules from action=help:
  - lowercase, [a-z0-9_]+, max 20 chars, max depth 3
  - global_unique_names across the whole tree (cities, people, items must
    not collide)
  - markdown links must resolve to files that already exist when checked

The script issues one batched POST that creates the directories, then the
city JSON files (so /osoby and /towary links resolve), then the people and
item files. Final action=done validates and emits the flag.
"""
from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
from pathlib import Path

import requests
from dotenv import load_dotenv

VERIFY_URL = "https://hub.ag3nts.org/verify"
LESSON_DIR = Path(__file__).parent

# --- canonical data (normalized — no Polish diacritics, singular nominative) ---

# city -> {item: quantity}  (parsed from ogloszenia.txt)
CITY_NEEDS: dict[str, dict[str, int]] = {
    "opalino":    {"chleb": 45,  "woda": 120, "mlotek": 6},
    "domatowo":   {"makaron": 60, "woda": 150, "lopata": 8},
    "brudzewo":   {"ryz": 55, "woda": 140, "wiertarka": 5},
    "darzlubie":  {"wolowina": 25, "woda": 130, "kilof": 7},
    "celbowo":    {"kurczak": 40, "woda": 125, "mlotek": 6},
    "mechowo":    {"ziemniak": 100, "kapusta": 70, "marchew": 65, "woda": 165, "lopata": 9},
    "puck":       {"chleb": 50, "ryz": 45, "woda": 175, "wiertarka": 7},
    "karlinkowo": {"makaron": 52, "wolowina": 22, "ziemniak": 95, "woda": 155, "kilof": 6},
}

# person filename -> (display name, city slug)  (parsed from rozmowy.txt)
PEOPLE: dict[str, tuple[str, str]] = {
    "natan_rams":    ("Natan Rams", "domatowo"),
    "iga_kapecka":   ("Iga Kapecka", "opalino"),
    "rafal_kisiel":  ("Rafal Kisiel", "brudzewo"),
    "marta_frantz":  ("Marta Frantz", "darzlubie"),
    "oskar_radtke":  ("Oskar Radtke", "celbowo"),
    "eliza_redmann": ("Eliza Redmann", "mechowo"),
    "damian_kroll":  ("Damian Kroll", "puck"),
    "lena_konkel":   ("Lena Konkel", "karlinkowo"),
}

# item slug -> list of city slugs offering it (parsed from transakcje.txt)
ITEM_SELLERS: dict[str, list[str]] = {
    "ryz":       ["darzlubie", "opalino", "karlinkowo"],
    "marchew":   ["puck"],
    "chleb":     ["domatowo", "celbowo", "brudzewo"],
    "wolowina":  ["opalino"],
    "kilof":     ["puck", "celbowo", "mechowo"],
    "wiertarka": ["karlinkowo", "domatowo"],
    "mlotek":    ["karlinkowo", "mechowo"],
    "makaron":   ["opalino"],
    "kapusta":   ["celbowo"],
    "ziemniak":  ["domatowo", "darzlubie"],
    "maka":      ["brudzewo", "mechowo"],
    "lopata":    ["brudzewo", "puck"],
    "kurczak":   ["darzlubie"],
}


def strip_diacritics(text: str) -> str:
    nfd = unicodedata.normalize("NFD", text)
    return ("".join(c for c in nfd if unicodedata.category(c) != "Mn")
            .replace("ł", "l").replace("Ł", "L"))


def display_city(slug: str) -> str:
    return slug.capitalize()


def city_md_link(slug: str) -> str:
    return f"[{display_city(slug)}](/miasta/{slug})"


def build_actions() -> list[dict]:
    actions: list[dict] = [{"action": "reset"}]

    for d in ("/miasta", "/osoby", "/towary"):
        actions.append({"action": "createDirectory", "path": d})

    # Cities first — links from /osoby and /towary need them to exist.
    for city, needs in CITY_NEEDS.items():
        actions.append({
            "action": "createFile",
            "path": f"/miasta/{city}",
            "content": json.dumps(needs, ensure_ascii=False, sort_keys=True),
        })

    for fname, (display, city) in PEOPLE.items():
        actions.append({
            "action": "createFile",
            "path": f"/osoby/{fname}",
            "content": f"{display}\n{city_md_link(city)}",
        })

    for item, cities in ITEM_SELLERS.items():
        body = "\n".join(city_md_link(c) for c in cities)
        actions.append({
            "action": "createFile",
            "path": f"/towary/{item}",
            "content": body,
        })

    return actions


def post(answer):
    payload = {
        "apikey": os.environ["CENTRALA_API_KEY"],
        "task": "filesystem",
        "answer": answer,
    }
    r = requests.post(VERIFY_URL, json=payload, timeout=60)
    try:
        return r.status_code, r.json()
    except ValueError:
        return r.status_code, {"raw": r.text}


def validate_against_notes() -> None:
    """Sanity-check that hardcoded data matches what's actually in the notes."""
    text = (LESSON_DIR / "transakcje.txt").read_text()
    line_re = re.compile(r"^(\S+)\s*->\s*(\S+)\s*->\s*(\S+)\s*$")
    actual: dict[str, set[str]] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        m = line_re.match(line)
        if not m:
            print(f"warning: unparsed transaction line: {line!r}", file=sys.stderr)
            continue
        seller, item, _ = m.groups()
        item_slug = strip_diacritics(item).lower()
        if item_slug == "ziemniaki":
            item_slug = "ziemniak"
        actual.setdefault(item_slug, set()).add(strip_diacritics(seller).lower())

    for item, expected_cities in ITEM_SELLERS.items():
        if set(expected_cities) != actual.get(item, set()):
            raise AssertionError(
                f"item {item}: hardcoded {expected_cities} != parsed {actual.get(item)}"
            )


def main() -> None:
    load_dotenv()
    if not os.environ.get("CENTRALA_API_KEY"):
        sys.exit("CENTRALA_API_KEY missing")

    print("validating hardcoded transactions against transakcje.txt…")
    validate_against_notes()
    print("ok")

    actions = build_actions()
    print(f"submitting batch with {len(actions)} actions…")
    status, body = post(actions)
    print(f"  -> HTTP {status}")
    print(json.dumps(body, ensure_ascii=False, indent=2)[:2000])

    # Batch returns code=100 ("Batch actions executed."); each result has its own code.
    if status >= 400 or body.get("code") not in (0, 100, None):
        sys.exit("batch failed; aborting before action=done")
    bad = [r for r in body.get("results", []) if r.get("code", 0) >= 400]
    if bad:
        print("batch sub-actions failed:", bad)
        sys.exit("aborting before action=done")

    print("\ncalling action=done…")
    status, body = post({"action": "done"})
    print(f"  -> HTTP {status}")
    print(json.dumps(body, ensure_ascii=False, indent=2))

    text = json.dumps(body, ensure_ascii=False)
    if "FLG" in text:
        print("\nFLAG received")
    else:
        print("\nno flag yet — check https://hub.ag3nts.org/filesystem_preview.html or "
              "the panel at https://hub.ag3nts.org/debug")


if __name__ == "__main__":
    main()
