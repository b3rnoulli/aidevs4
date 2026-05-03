"""Time-machine pilot — assistant for task `timetravel`.

The device API exposes only help / getConfig / reset / configure(day, month,
year, syncRatio, stabilization). PT-A, PT-B, PWR and standby/active live in
the web preview (https://hub.ag3nts.org/timetravel_preview) and must be
toggled by a human operator. This script is a thin client: it does the math
(syncRatio + Polish-prose stabilization hint), POSTs configuration, polls
state, and prompts the operator at each manual step.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

TASK = "timetravel"
VERIFY_URL = "https://hub.ag3nts.org/verify"
DOCS_URL = "https://hub.ag3nts.org/dane/timetravel.md"
PREVIEW_URL = "https://hub.ag3nts.org/timetravel_preview"
LESSON_DIR = Path(__file__).parent
DOCS_PATH = LESSON_DIR / "timetravel.md"
FLAG_RE = re.compile(r"\{FLG:[^}]+\}")

TODAY: tuple[int, int, int] = (2026, 5, 3)
JUMPS: dict[int, tuple[int, int, int]] = {
    1: (2238, 11, 5),
    2: TODAY,
    3: (2024, 11, 12),
}
JUMP_DESCRIPTIONS = {
    1: "JUMP 1 -> 2238-11-05 (pick up fresh batteries; PT-A only)",
    2: "JUMP 2 -> today 2026-05-03 (return to present; PT-A only)",
    3: "JUMP 3 -> 2024-11-12 (open time tunnel; PT-A AND PT-B)",
}


def _load_env() -> None:
    here = Path(__file__).resolve()
    for path in (here.parents[2] / ".env", here.parents[5] / ".env"):
        if path.exists():
            load_dotenv(path)
    if not os.environ.get("CENTRALA_API_KEY"):
        print("CENTRALA_API_KEY missing", file=sys.stderr)
        sys.exit(2)


def _api_key() -> str:
    return os.environ["CENTRALA_API_KEY"]


def _post(answer: dict, *, timeout: int = 30) -> dict:
    payload = {"apikey": _api_key(), "task": TASK, "answer": answer}
    response = requests.post(VERIFY_URL, json=payload, timeout=timeout)
    try:
        return response.json()
    except ValueError:
        return {"_http_status": response.status_code, "_text": response.text}


def _pretty(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


# ---------- Polish number parsing for the stabilization hint ----------
PL_UNITS = {
    "zero": 0, "jeden": 1, "dwa": 2, "trzy": 3, "cztery": 4,
    "pięć": 5, "sześć": 6, "siedem": 7, "osiem": 8, "dziewięć": 9,
}
PL_TEEN = {
    "dziesięć": 10, "jedenaście": 11, "dwanaście": 12, "trzynaście": 13,
    "czternaście": 14, "piętnaście": 15, "szesnaście": 16, "siedemnaście": 17,
    "osiemnaście": 18, "dziewiętnaście": 19,
}
PL_TENS = {
    "dwadzieścia": 20, "trzydzieści": 30, "czterdzieści": 40, "pięćdziesiąt": 50,
    "sześćdziesiąt": 60, "siedemdziesiąt": 70, "osiemdziesiąt": 80, "dziewięćdziesiąt": 90,
}
PL_HUNDREDS = {
    "sto": 100, "dwieście": 200, "trzysta": 300, "czterysta": 400,
    "pięćset": 500, "sześćset": 600, "siedemset": 700, "osiemset": 800, "dziewięćset": 900,
}
PL_THOUSAND = {"tysiąc": 1000, "tysiące": 1000, "tysięcy": 1000}
ALL_NUM_WORDS = {**PL_UNITS, **PL_TEEN, **PL_TENS, **PL_HUNDREDS, **PL_THOUSAND}


def _parse_polish_number_run(words: list[str]) -> int | None:
    """Parse a sequence of consecutive Polish number-words into one integer.
    Handles 0..1000 as: [thousand] [hundreds] [tens|teen] [units]."""
    total = 0
    matched = False
    for w in words:
        if w in PL_THOUSAND:
            total += 1000
            matched = True
        elif w in PL_HUNDREDS:
            total += PL_HUNDREDS[w]
            matched = True
        elif w in PL_TEEN:
            total += PL_TEEN[w]
            matched = True
        elif w in PL_TENS:
            total += PL_TENS[w]
            matched = True
        elif w in PL_UNITS:
            total += PL_UNITS[w]
            matched = True
        else:
            return None
    return total if matched else None


def _scan_numbers(text: str) -> list[tuple[int, int, int]]:
    """Find all Polish-number runs in `text`. Return [(start, end, value)]."""
    tokens = re.findall(r"[A-Za-zÀ-ɏąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+|\d+", text)
    spans: list[tuple[int, int, int]] = []
    pos = 0
    run: list[tuple[int, str]] = []
    for tok in tokens:
        idx = text.find(tok, pos)
        pos = idx + len(tok)
        low = tok.lower()
        if low in ALL_NUM_WORDS:
            run.append((idx, low))
        else:
            if run:
                value = _parse_polish_number_run([w for _, w in run])
                if value is not None:
                    spans.append((run[0][0], run[-1][0] + len(run[-1][1]), value))
                run = []
            if tok.isdigit():
                spans.append((idx, idx + len(tok), int(tok)))
    if run:
        value = _parse_polish_number_run([w for _, w in run])
        if value is not None:
            spans.append((run[0][0], run[-1][0] + len(run[-1][1]), value))
    return spans


def parse_stabilization_hint(text: str) -> int | None:
    """Read the device's Polish stabilization advice and compute a number.

    First Polish-number-or-digit found is the base. For each subsequent
    number, look at the preceding ~150 chars: detect a verb stem
    (subtract/add/divide/multiply) and the connector ('o' / 'przez') to
    decide which operation to apply.
    """
    if not text:
        return None
    spans = _scan_numbers(text)
    if not spans:
        return None
    base = spans[0][2]
    result: float = base
    lower = text.lower()
    SUB = re.compile(r"\b(?:obniż\w*|zmniejsz\w*|odjąć|odejm\w*)\b")
    ADD = re.compile(r"\b(?:podwyższ\w*|zwiększ\w*|dodać|dodaj\w*|podnie\w*)\b")
    DIV = re.compile(r"\b(?:podziel\w*|podzielon\w*|podział\w*)\b")
    MUL = re.compile(r"\b(?:pomnoż\w*|przemnoż\w*|razy)\b")
    O_CONN = re.compile(r"\bo(?:\s+około)?\s*$")
    PRZEZ = re.compile(r"\bprzez\s*$")
    for start, _end, value in spans[1:]:
        before = lower[:start].rstrip()
        ctx = before[-150:]
        immediate = before[-30:]
        if SUB.search(ctx) and O_CONN.search(immediate):
            result -= value
        elif ADD.search(ctx) and O_CONN.search(immediate):
            result += value
        elif DIV.search(ctx) and PRZEZ.search(immediate):
            if value:
                result /= value
        elif MUL.search(ctx) and PRZEZ.search(immediate):
            result *= value
        else:
            # Unknown relation: stop combining
            break
    return int(round(result))


# ---------- PWR (ochrona) lookup parsed from the cached docs ----------
_PWR_CACHE: dict[int, int] | None = None


def _load_pwr_table() -> dict[int, int]:
    global _PWR_CACHE
    if _PWR_CACHE is not None:
        return _PWR_CACHE
    table: dict[int, int] = {}
    if DOCS_PATH.exists():
        for line in DOCS_PATH.read_text().splitlines():
            if "|" not in line:
                continue
            cells = [c.strip() for c in line.split("|") if c.strip()]
            # rows are "year value year value ..." in pairs of 10
            if len(cells) >= 2 and cells[0].isdigit() and 1500 <= int(cells[0]) <= 2499:
                # iterate as pairs
                for i in range(0, len(cells) - 1, 2):
                    a, b = cells[i], cells[i + 1]
                    if a.isdigit() and b.isdigit():
                        table[int(a)] = int(b)
    _PWR_CACHE = table
    return table


def lookup_pwr(year: int) -> int | None:
    return _load_pwr_table().get(year)


# ---------- core API helpers ----------
def get_config() -> dict:
    return _post({"action": "getConfig"})


def configure(param: str, value: Any, *, quiet: bool = False) -> dict:
    if not quiet:
        print(f"  configure({param}={value!r})")
    data = _post({"action": "configure", "param": param, "value": value})
    if not quiet:
        msg = data.get("message")
        cfg = data.get("config", {}) if isinstance(data, dict) else {}
        flux = cfg.get("fluxDensity")
        cond = cfg.get("condition")
        print(f"    -> code={data.get('code')} msg={msg!r} flux={flux} cond={cond}")
        if "needConfig" in data:
            print(f"    -> needConfig: {data['needConfig']}")
    return data


def compute_sync_ratio(year: int, month: int, day: int) -> float:
    return ((day * 8 + month * 12 + year * 7) % 101) / 100.0


def find_flag(payload: Any) -> str | None:
    match = FLAG_RE.search(json.dumps(payload, ensure_ascii=False))
    return match.group(0) if match else None


def _internal_mode_for_year(year: int) -> set[int]:
    if year < 2000:
        return {1}
    if year <= 2150:
        return {2}
    if year <= 2300:
        return {3}
    return {4}


def _print_state(cfg: dict) -> None:
    print(_pretty(cfg))


def operator_prompt(label: str) -> None:
    try:
        input(f"\n[OPERATOR] {label}\n          press Enter when done... ")
    except EOFError:
        print(" (no TTY; continuing)")


# ---------- subcommands ----------
def cmd_help(args: argparse.Namespace) -> int:
    print(_pretty(_post({"action": "help"})))
    if not DOCS_PATH.exists():
        try:
            response = requests.get(DOCS_URL, timeout=30)
            response.raise_for_status()
            DOCS_PATH.write_text(response.text)
            print(f"\n[cache] wrote {DOCS_PATH}")
        except requests.RequestException as exc:
            print(f"\n[cache] failed to fetch {DOCS_URL}: {exc}", file=sys.stderr)
    return 0


def cmd_get_config(args: argparse.Namespace) -> int:
    print(_pretty(get_config()))
    return 0


def cmd_reset(args: argparse.Namespace) -> int:
    print(_pretty(_post({"action": "reset"})))
    return 0


def cmd_set(args: argparse.Namespace) -> int:
    value: Any = args.value
    if args.param in {"day", "month", "year", "stabilization"}:
        value = int(value)
    elif args.param == "syncRatio":
        value = float(value)
    print(_pretty(configure(args.param, value)))
    return 0


def cmd_sync_ratio(args: argparse.Namespace) -> int:
    parts = args.date.split("-")
    y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
    print(f"syncRatio({y:04d}-{m:02d}-{d:02d}) = {compute_sync_ratio(y, m, d):.2f}")
    return 0


def cmd_pwr(args: argparse.Namespace) -> int:
    pwr = lookup_pwr(int(args.year))
    if pwr is None:
        print("not found", file=sys.stderr)
        return 1
    print(pwr)
    return 0


def cmd_set_date(args: argparse.Namespace) -> int:
    parts = args.date.split("-")
    y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
    return _set_date_and_stabilize(y, m, d)


def _set_date_and_stabilize(year: int, month: int, day: int) -> int:
    print(f"\n[step] configure date {year:04d}-{month:02d}-{day:02d}")
    configure("day", day)
    configure("month", month)
    last = configure("year", year)
    sr = round(compute_sync_ratio(year, month, day), 2)
    configure("syncRatio", sr)
    hint_text = (last or {}).get("needConfig") or ""
    if not hint_text:
        # rare: hint may surface only after one of the later configures.
        last2 = get_config()
        hint_text = last2.get("needConfig", "") if isinstance(last2, dict) else ""
    if hint_text:
        print(f"\n[stabilization hint] {hint_text}")
        value = parse_stabilization_hint(hint_text)
        if value is None:
            print(
                "[stabilization] could not parse Polish hint; "
                "rerun `set stabilization VALUE` manually."
            )
            return 1
        print(f"[stabilization] parsed value = {value}")
        configure("stabilization", value)
    else:
        print("[stabilization] no hint surfaced — leaving as-is.")
    cfg = get_config().get("config", {})
    print("\n[state]")
    _print_state(cfg)
    return 0


def cmd_pilot(args: argparse.Namespace) -> int:
    jumps = [args.jump] if args.jump else [1, 2, 3]
    for n in jumps:
        rc = run_jump(n, today_override=args.today)
        if rc != 0:
            return rc
    return 0


def run_jump(n: int, *, today_override: str | None) -> int:
    if today_override and n == 2:
        parts = today_override.split("-")
        y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
    else:
        y, m, d = JUMPS[n]
    print("=" * 70)
    print(JUMP_DESCRIPTIONS[n])
    print(f"target date: {y:04d}-{m:02d}-{d:02d}")
    print("=" * 70)

    pre_cfg = get_config().get("config", {})
    pre_date = pre_cfg.get("currentDate")
    print(f"\n[pre-state] currentDate={pre_date} battery={pre_cfg.get('batteryStatus')}")

    rc = _set_date_and_stabilize(y, m, d)
    if rc != 0:
        return rc

    pwr = lookup_pwr(y)
    pt_b = "ON" if n == 3 else "OFF"
    operator_prompt(
        f"open {PREVIEW_URL}\n"
        f"          - confirm device is in STANDBY\n"
        f"          - set PWR slider to {pwr}\n"
        f"          - set PT-A = ON\n"
        f"          - set PT-B = {pt_b}"
    )

    target_modes = _internal_mode_for_year(y)
    print(f"\n[step] poll until internalMode in {target_modes} and flux=100%")
    cfg = wait_for_active_window(target_modes, timeout=240)
    if cfg is None:
        print("timed out waiting for activate window", file=sys.stderr)
        return 1
    print("\n[state right before activate]")
    _print_state(cfg)

    operator_prompt(
        "switch device from STANDBY to ACTIVE in the preview UI now "
        "(while internalMode is still in range and flux=100%)"
    )

    print("\n[step] poll for currentDate change / flag")
    cfg = wait_for_arrival(pre_date, timeout=180)
    print("\n[final state]")
    _print_state(cfg)
    flag = find_flag(cfg)
    if flag:
        print(f"\nFLAG: {flag}")
    return 0


def wait_for_active_window(target_modes: set[int], *, timeout: int) -> dict | None:
    deadline = time.monotonic() + timeout
    last_snapshot: tuple[Any, Any, Any] | None = None
    while time.monotonic() < deadline:
        full = get_config()
        cfg = full.get("config", {}) if isinstance(full, dict) else {}
        mode = cfg.get("internalMode")
        flux = cfg.get("fluxDensity")
        cond = cfg.get("condition")
        snap = (mode, flux, cond)
        if snap != last_snapshot:
            print(f"  internalMode={mode} flux={flux} condition={cond} "
                  f"PWR={cfg.get('PWR')} PTA={cfg.get('PTA')} PTB={cfg.get('PTB')}")
            last_snapshot = snap
        if mode in target_modes and flux == 100:
            return cfg
        time.sleep(2)
    return None


def wait_for_arrival(prev_date: Any, *, timeout: int) -> dict:
    deadline = time.monotonic() + timeout
    last_snapshot: tuple[Any, Any, Any] | None = None
    cfg: dict = {}
    while time.monotonic() < deadline:
        full = get_config()
        cfg = full.get("config", {}) if isinstance(full, dict) else {}
        cur = cfg.get("currentDate")
        mode_pos = cfg.get("mode")
        flux = cfg.get("fluxDensity")
        snap = (cur, mode_pos, flux)
        if snap != last_snapshot:
            print(f"  currentDate={cur} mode={mode_pos} flux={flux} "
                  f"battery={cfg.get('batteryStatus')}")
            last_snapshot = snap
        if find_flag(full):
            return full
        if cur and cur != prev_date:
            return full
        time.sleep(2)
    return cfg


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Time-machine pilot CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("help").set_defaults(func=cmd_help)
    sub.add_parser("get-config").set_defaults(func=cmd_get_config)
    sub.add_parser("reset").set_defaults(func=cmd_reset)

    p_set = sub.add_parser("set", help="configure one parameter")
    p_set.add_argument(
        "param", choices=["day", "month", "year", "syncRatio", "stabilization"]
    )
    p_set.add_argument("value")
    p_set.set_defaults(func=cmd_set)

    p_sd = sub.add_parser(
        "set-date",
        help="configure day, month, year, syncRatio, stabilization for a date",
    )
    p_sd.add_argument("date")
    p_sd.set_defaults(func=cmd_set_date)

    p_sr = sub.add_parser("sync-ratio", help="compute sync ratio locally")
    p_sr.add_argument("date")
    p_sr.set_defaults(func=cmd_sync_ratio)

    p_pwr = sub.add_parser("pwr", help="look up PWR for a year (from cached docs)")
    p_pwr.add_argument("year")
    p_pwr.set_defaults(func=cmd_pwr)

    p_pilot = sub.add_parser("pilot", help="guided jump walkthrough")
    p_pilot.add_argument("--jump", type=int, choices=[1, 2, 3])
    p_pilot.add_argument("--today")
    p_pilot.set_defaults(func=cmd_pilot)

    args = parser.parse_args(argv)
    _load_env()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
