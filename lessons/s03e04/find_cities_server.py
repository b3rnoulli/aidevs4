"""Tool endpoint for the `negotiations` task.

Exposes POST /api/find-cities, which takes a natural-language description of
an item (e.g. "potrzebuję turbiny wiatrowej 48V") and returns the list of
cities where that item is available, looked up against the bundled CSV
knowledge base (cities.csv, items.csv, connections.csv from
https://hub.ag3nts.org/dane/s03e04_csv/).

Matching is deterministic Polish-aware: lowercased, diacritics stripped,
prefix overlap on tokens, with exact matching of unit tokens like "48V",
"400W", "150Ah". No LLM is used — the items list is regular and the agent's
queries are predictable enough that token scoring is reliable, and avoiding
the LLM keeps responses well under the 500-byte tool-output cap.

Listens on PORT (default 3000) so the ngrok tunnel forwards to it.
"""
from __future__ import annotations

import csv
import json
import re
import sys
import unicodedata
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORT = 3000
CSV_DIR = Path(__file__).parent
MAX_OUTPUT_BYTES = 500
TOP_RESULTS = 3

UNIT_RE = re.compile(r"\b\d+(?:[.,]\d+)?\s*(?:v|w|a|ah|kohm|ohm|mhz|khz|hz|nf|pf|uf|mf|f|h|kg|m|cm|mm)\b", re.IGNORECASE)
WORD_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)


def _log(*args: object) -> None:
    print(*args, file=sys.stderr, flush=True)


def strip_diacritics(text: str) -> str:
    nfd = unicodedata.normalize("NFD", text)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn").replace("ł", "l").replace("Ł", "L")


def normalize(text: str) -> str:
    return strip_diacritics(text).lower()


def tokenize(text: str) -> tuple[list[str], list[str]]:
    """Return (units, words). Units are kept verbatim for exact matching."""
    norm = normalize(text)
    units = [m.group(0).replace(" ", "").replace(",", ".") for m in UNIT_RE.finditer(norm)]
    words = [w for w in WORD_RE.findall(norm) if len(w) >= 3]
    return units, words


def load_data() -> tuple[dict[str, str], dict[str, str], dict[str, list[str]]]:
    """Returns (city_code_to_name, item_code_to_name, item_code_to_city_codes)."""
    cities = {}
    with (CSV_DIR / "cities.csv").open() as f:
        for row in csv.DictReader(f):
            cities[row["code"]] = row["name"]

    items = {}
    with (CSV_DIR / "items.csv").open() as f:
        for row in csv.DictReader(f):
            items[row["code"]] = row["name"]

    item_to_cities: dict[str, list[str]] = {}
    with (CSV_DIR / "connections.csv").open() as f:
        for row in csv.DictReader(f):
            item_to_cities.setdefault(row["itemCode"], []).append(row["cityCode"])

    return cities, items, item_to_cities


def precompute_item_tokens(items: dict[str, str]) -> dict[str, tuple[set[str], list[str]]]:
    """For each item code, precompute its (unit_set, word_list)."""
    out = {}
    for code, name in items.items():
        units, words = tokenize(name)
        out[code] = (set(units), words)
    return out


def token_match_score(query_word: str, item_word: str) -> int:
    """Return a small int score for prefix/substring overlap between two normalized words.

    Encourages matching Polish stems: 'turbiny' vs 'turbina' share 'turbin'.
    """
    if query_word == item_word:
        return 3
    n = min(len(query_word), len(item_word))
    if n < 4:
        return 0
    # Prefix match
    common = 0
    for i in range(n):
        if query_word[i] == item_word[i]:
            common += 1
        else:
            break
    if common >= 5:
        return 2
    if common >= 4:
        return 1
    # Substring fallback
    if len(query_word) >= 5 and query_word in item_word:
        return 2
    if len(item_word) >= 5 and item_word in query_word:
        return 2
    return 0


def score_item(query_units: list[str], query_words: list[str],
               item_units: set[str], item_words: list[str]) -> int:
    score = 0
    # Unit tokens — strong signal, exact match required
    for u in query_units:
        if u in item_units:
            score += 5
    # Word tokens — best per query word
    for qw in query_words:
        best = 0
        for iw in item_words:
            best = max(best, token_match_score(qw, iw))
        score += best
    return score


def find_matches(query: str, items: dict[str, str],
                 item_tokens: dict[str, tuple[set[str], list[str]]],
                 top_k: int = TOP_RESULTS) -> list[tuple[int, str, str]]:
    """Return list of (score, item_code, item_name) with top-k highest scores (>0)."""
    query_units, query_words = tokenize(query)
    if not query_units and not query_words:
        return []
    scored = []
    for code, name in items.items():
        units, words = item_tokens[code]
        s = score_item(query_units, query_words, units, words)
        if s > 0:
            scored.append((s, code, name))
    scored.sort(key=lambda x: (-x[0], x[2]))
    if not scored:
        return []
    top_score = scored[0][0]
    # Keep only items at or near the top score, capped at top_k
    return [(s, c, n) for (s, c, n) in scored if s >= max(top_score - 2, 1)][:top_k]


def format_output(matches: list[tuple[int, str, str]],
                  items_to_cities: dict[str, list[str]],
                  cities: dict[str, str]) -> str:
    """Render a compact response under MAX_OUTPUT_BYTES."""
    if not matches:
        return "Nie znaleziono pasujacego przedmiotu. Doprecyzuj nazwe."

    # When the top score dominates, return one item with its cities.
    # When multiple similar items match (e.g. 12V vs 48V variants), list each.
    lines = []
    for _score, code, name in matches:
        city_codes = items_to_cities.get(code, [])
        city_names = [cities.get(cc, cc) for cc in city_codes]
        if city_names:
            lines.append(f"{name}: {', '.join(city_names)}")
        else:
            lines.append(f"{name}: brak miast")

    out = " | ".join(lines)
    if len(out.encode("utf-8")) > MAX_OUTPUT_BYTES:
        # Trim to first match only.
        out = lines[0]
        if len(out.encode("utf-8")) > MAX_OUTPUT_BYTES:
            # Last resort — truncate.
            while len(out.encode("utf-8")) > MAX_OUTPUT_BYTES - 1:
                out = out[:-1]
    return out


CITIES, ITEMS, ITEMS_TO_CITIES = {}, {}, {}
ITEM_TOKENS: dict[str, tuple[set[str], list[str]]] = {}


def handle_query(query: str) -> str:
    matches = find_matches(query, ITEMS, ITEM_TOKENS)
    return format_output(matches, ITEMS_TO_CITIES, CITIES)


class Handler(BaseHTTPRequestHandler):
    server_version = "find-cities/1.0"

    def log_message(self, fmt: str, *args) -> None:
        _log("[http]", self.address_string(), fmt % args)

    def _write_json(self, status: int, body: dict) -> None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("ngrok-skip-browser-warning", "true")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        body = b"find-cities ok\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("ngrok-skip-browser-warning", "true")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        try:
            length = int(self.headers.get("Content-Length") or "0")
            raw = self.rfile.read(length) if length > 0 else b""
            try:
                payload = json.loads(raw.decode("utf-8")) if raw else {}
            except (ValueError, UnicodeDecodeError) as exc:
                _log(f"bad json: {exc}")
                self._write_json(400, {"output": "Bledny JSON"})
                return

            query = payload.get("params") or payload.get("query") or ""
            if not isinstance(query, str) or not query.strip():
                self._write_json(200, {"output": "Podaj nazwe przedmiotu w polu params."})
                return

            _log(f"[in ] {query!r}")
            output = handle_query(query)
            _log(f"[out] ({len(output.encode('utf-8'))} bytes) {output!r}")
            self._write_json(200, {"output": output})
        except Exception as exc:
            _log(f"handler error: {exc!r}")
            try:
                self._write_json(500, {"output": "Blad serwera"})
            except Exception:
                pass


def main() -> None:
    global CITIES, ITEMS, ITEMS_TO_CITIES, ITEM_TOKENS
    CITIES, ITEMS, ITEMS_TO_CITIES = load_data()
    ITEM_TOKENS = precompute_item_tokens(ITEMS)
    _log(f"loaded {len(CITIES)} cities, {len(ITEMS)} items, "
         f"{sum(len(v) for v in ITEMS_TO_CITIES.values())} connections")

    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    _log(f"listening on http://0.0.0.0:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        _log("shutting down")
        server.server_close()


if __name__ == "__main__":
    main()
