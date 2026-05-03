"""S02E03 — Condense the power plant failure log and submit it to Centrala.

Pipeline:
1. Download failure.log from hub.ag3nts.org (cached locally).
2. Cheap regex pre-filter to severity >= WARN.
3. Algorithmic condensation (one line per unique signature, text shortening).
4. Optional Gemini polish/expansion driven by Centrala feedback.
5. Conservative token check (chars/3.5).
6. Submit to Centrala /verify; iterate with technician feedback until {FLG:...}.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

from aidevs4.centrala import submit_answer

LESSON_DIR = Path(__file__).resolve().parent
RAW_LOG = LESSON_DIR / "failure.log"
FILTERED_LOG = LESSON_DIR / "failure.filtered.log"
CONDENSED_LOG = LESSON_DIR / "failure.condensed.log"
HISTORY_FILE = LESSON_DIR / "feedback_history.txt"

TASK_NAME = "failure"
DOWNLOAD_URL_TEMPLATE = "https://hub.ag3nts.org/data/{key}/failure.log"

SEVERE_LEVEL_RE = re.compile(
    r"\[(WARN(?:ING)?|ERR(?:O|OR)?|CRIT(?:ICAL)?|FATAL|ALERT|EMERG(?:ENCY)?)\]",
    re.IGNORECASE,
)

TOKEN_HARD_LIMIT = 1500
TOKEN_TARGET = 1300
TOKEN_RETRY_TARGET = 1100
# Empirically calibrated against Centrala's tokenizer feedback: 4924 chars -> 1692 tokens,
# i.e. ~2.91 chars/token. Use 2.8 for an extra safety margin.
TOKEN_CHARS_PER_TOKEN = 2.8
# Targeted char output to land safely under the 1500-token cap.
OUTPUT_CHAR_TARGET = 3700  # ~1320 tokens at 2.8 c/t
OUTPUT_CHAR_HARD_CAP = 4000  # ~1430 tokens — leaves a small margin

GEMINI_MODEL_PREFERENCE = (
    "gemini-2.5-flash-lite",  # separate free-tier quota pool
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
)
GEMINI_429_MAX_RETRIES = 2

FLAG_RE = re.compile(r"\{FLG:[^}]+\}")


def estimate_tokens(text: str) -> int:
    return math.ceil(len(text) / TOKEN_CHARS_PER_TOKEN)


def load_env() -> None:
    """Load .env from worktree, then fall back to the main repo .env."""
    repo_root = Path(__file__).resolve().parents[2]
    load_dotenv(repo_root / ".env")
    load_dotenv(repo_root.parent.parent.parent / ".env")


def download_log(api_key: str, *, refresh: bool) -> str:
    if RAW_LOG.exists() and not refresh:
        text = RAW_LOG.read_text(encoding="utf-8", errors="replace")
        print(f"[download] cache hit: {RAW_LOG} ({len(text):,} chars)")
        return text

    url = DOWNLOAD_URL_TEMPLATE.format(key=api_key)
    print(f"[download] fetching {url}")
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    text = response.text
    RAW_LOG.write_text(text, encoding="utf-8")
    print(f"[download] saved {len(text):,} chars to {RAW_LOG}")
    return text


_TIMESTAMP_RE = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]\s*")


def _line_signature(line: str) -> str:
    """Strip timestamp so we can detect repeated identical events."""
    return _TIMESTAMP_RE.sub("", line).strip()


_LEVEL_RE = re.compile(r"\[(WARN(?:ING)?|ERR(?:O|OR)?|CRIT(?:ICAL)?|FATAL|ALERT|EMERG(?:ENCY)?|INFO|DEBUG|TRACE|NOTICE)\]", re.IGNORECASE)


def _line_level(line: str) -> str | None:
    m = _LEVEL_RE.search(line)
    return m.group(1).upper() if m else None


def pre_filter(raw: str) -> str:
    severe: list[str] = []
    for line in raw.splitlines():
        if SEVERE_LEVEL_RE.search(line):
            severe.append(line.rstrip())

    # Strategy: keep every CRIT/ERR line individually (these are the failure trail);
    # for WARN, keep the first and last occurrence per signature so the LLM still
    # sees coverage and time-ranging without duplicate noise.
    high = {"CRIT", "CRITICAL", "FATAL", "ALERT", "EMERG", "EMERGENCY", "ERR", "ERRO", "ERROR"}
    first_warn: dict[str, str] = {}
    last_warn: dict[str, str] = {}
    high_lines: list[str] = []

    for line in severe:
        level = _line_level(line) or ""
        if level in high:
            high_lines.append(line)
        else:
            sig = _line_signature(line)
            first_warn.setdefault(sig, line)
            last_warn[sig] = line

    # Combine and re-sort by timestamp so the LLM sees a chronological narrative.
    combined: list[str] = list(high_lines)
    for sig, first in first_warn.items():
        combined.append(first)
        last = last_warn[sig]
        if last != first:
            combined.append(last)

    def _ts_key(line: str) -> str:
        return line[:21]  # "[YYYY-MM-DD HH:MM:SS]"

    combined.sort(key=_ts_key)

    out = "\n".join(combined)
    FILTERED_LOG.write_text(out, encoding="utf-8")
    print(
        f"[filter] severe={len(severe):,} (CRIT/ERR={len(high_lines):,}, "
        f"unique WARN sigs={len(first_warn):,}); kept {len(combined):,} lines "
        f"(~{estimate_tokens(out):,} est. tokens) -> {FILTERED_LOG}"
    )
    return out


def build_prompt(filtered: str, feedback: str | None) -> str:
    parts = [
        "You are condensing a power-plant syslog for technicians who must analyze a "
        "shutdown that happened around 22:00 after a startup at ~06:00.",
        "",
        "RULES:",
        "- Output ONLY a multi-line incident timeline. No prose, no headers, no commentary, no markdown fences.",
        "- Strict per-line format: `[YYYY-MM-DD HH:MM] [LEVEL] COMPONENT_ID short description.`",
        "- Drop seconds from the timestamp (source has HH:MM:SS — output HH:MM).",
        "- Preserve severity LEVEL and the COMPONENT_ID/identifier verbatim from the source.",
        "- Keep ONLY events relevant to failure analysis: power generation, distribution, "
        "transformers/inverters, cooling loops, water pumps and tanks, reactor/turbine "
        "subsystems, sensors, control software (FIRMWARE), safety interlocks, waste handling, "
        "communication buses/controllers, and other plant subsystems.",
        "- Group near-duplicate repeated events: keep the first occurrence at its earliest time, "
        "or the most severe one if levels differ. You may merge a run of identical warnings "
        "into a single line that says e.g. 'recurring through HH:MM'.",
        "- Order chronologically by timestamp.",
        f"- HARD CAP: total output must be under {OUTPUT_CHAR_HARD_CAP} characters (~1300 tokens). "
        f"Aim for around {OUTPUT_CHAR_TARGET} characters.",
        "- Coverage matters: include EVERY distinct component that produced a severe event "
        "(WARN/ERR/CRIT). Breadth of components > verbosity of any single line.",
        "- Always include the FIRST and LAST severe event for each component, and any CRIT/ERROR "
        "events in between, plus the trip/shutdown event.",
        "- Be terse. Drop filler words. Use abbreviations when unambiguous.",
    ]
    if feedback:
        parts += [
            "",
            "TECHNICIAN FEEDBACK ON PREVIOUS SUBMISSION (use it to fix the next answer):",
            feedback.strip(),
        ]
    parts += [
        "",
        "PRE-FILTERED SEVERE LOG LINES (source material, already filtered to WARN+):",
        "```",
        filtered,
        "```",
        "",
        "Return ONLY the condensed timeline lines, nothing else.",
    ]
    return "\n".join(parts)


def _generate_once(client: genai.Client, model: str, prompt: str):
    return client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="text/plain",
            temperature=0.2,
        ),
    )


def gemini_condense(client: genai.Client, prompt: str) -> str:
    """Try each model in preference order; on 429 retry with backoff, then fall through."""
    last_error: Exception | None = None
    response = None
    for model in GEMINI_MODEL_PREFERENCE:
        for attempt in range(GEMINI_429_MAX_RETRIES + 1):
            try:
                response = _generate_once(client, model, prompt)
                if model != GEMINI_MODEL_PREFERENCE[0] or attempt > 0:
                    print(f"[gemini] succeeded with model={model}")
                last_error = None
                break
            except Exception as e:  # noqa: BLE001
                last_error = e
                msg = str(e)
                is_429 = "429" in msg or "RESOURCE_EXHAUSTED" in msg
                if not is_429:
                    raise
                wait = 30.0
                m = re.search(r"retry in (\d+(?:\.\d+)?)s", msg)
                if m:
                    wait = float(m.group(1)) + 1.0
                if attempt >= GEMINI_429_MAX_RETRIES:
                    print(f"[gemini] {model}: 429 quota persists; trying next model")
                    break
                # Per-minute rate limits report waits in tens of seconds; honour them.
                # Per-day quotas report waits in thousands of seconds — those we skip.
                if wait > 90:
                    print(f"[gemini] {model}: 429 (retry in {wait:.0f}s); skipping to next model")
                    break
                print(f"[gemini] {model}: 429; sleeping {wait:.1f}s (attempt {attempt + 1})")
                time.sleep(wait)
        if response is not None:
            break
    if response is None:
        raise last_error if last_error else RuntimeError("Gemini failed for all candidate models")
    text = (response.text or "").strip()
    # Strip ```...``` fences if Gemini wrapped them.
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


def shrink_with_llm(client: genai.Client, condensed: str, target_chars: int) -> str:
    prompt = (
        "You produced a condensed power-plant incident log, but it is still too long. "
        f"Compress it further to under {target_chars} characters total. "
        "Keep the same per-line format `[YYYY-MM-DD HH:MM] [LEVEL] COMPONENT_ID short description.` "
        "Keep EVERY distinct COMPONENT_ID that appears at least once. "
        "Shorten descriptions, merge consecutive near-duplicate warnings into a single line "
        "(e.g. 'recurring through HH:MM'), drop low-value warnings if needed, "
        "but keep all CRIT/ERR events. Return only the lines, no prose, no fences.\n\n"
        f"CURRENT LOG:\n```\n{condensed}\n```"
    )
    return gemini_condense(client, prompt)


_LINE_RE = re.compile(
    r"^\[(\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2}):(\d{2})\]\s*\[([A-Z]+)\]\s*(.*)$"
)

_FILLER_RES = [
    (re.compile(r"\b(is|are|was|were|has|have|been|being|the|a|an)\b\s*", re.IGNORECASE), ""),
    (re.compile(r"\b(remains?|continues?|appears?)\s+to\s+", re.IGNORECASE), ""),
    (re.compile(r"\bremain(?:s)?\b\s*", re.IGNORECASE), ""),
    (re.compile(r"\s+"), " "),
]

# Higher-impact phrase shortenings tuned to this log's vocabulary.
_PHRASE_SHORTENINGS = [
    ("below critical threshold", "<crit"),
    ("below critical reserve for sustained operation", "<crit reserve"),
    ("below operational target", "<op target"),
    ("approaching soft cap", "near soft cap"),
    ("crossed warning limits", "crossed WARN limits"),
    ("exceeds advisory threshold", "> advisory"),
    ("failed recovery step in active sequence", "failed recovery step"),
    ("exceeded correction budget", "> corr budget"),
    ("returned nonblocking fault set", "nonblocking fault set"),
    ("Heat transfer path to", "Heat path to"),
    ("Coolant level in", "Coolant in"),
    ("Coolant inventory in", "Coolant inv in"),
    ("Fill trajectory in", "Fill traj in"),
    ("Flow margin on", "Flow margin"),
    ("Pressure jitter near", "Pressure jitter"),
    ("Thermal drift on", "Thermal drift"),
    ("Input ripple on", "Input ripple"),
    ("Cooling efficiency on", "Cooling eff on"),
    ("absorption path reached emergency boundary", "absorption -> emergency"),
    ("reactor protection initiates critical stop", "reactor crit stop"),
    ("entered emergency guard branch after repeated safety faults", "emergency guard, safety faults"),
    ("can no longer sustain stable feed for cooling auxiliaries", "can't feed cooling aux"),
    ("lost stable prime under peak thermal demand", "lost prime, peak demand"),
    ("reported runaway outlet temperature", "runaway outlet temp"),
    ("decoupling sequence forced by thermal risk", "decoupled, thermal risk"),
    ("Coolant inventory in WTANK07 below critical threshold for full-loop operation", "WTANK07 coolant <crit, full-loop"),
    ("Insufficient cooling capacity confirmed after incomplete WTANK07 refill", "Insufficient cooling, incomplete refill"),
    ("Final trip complete because WTANK07 remained under critical water level", "Final trip: WTANK07 <crit water"),
    ("Critical boundary exceeded on", "Crit boundary on"),
    ("core cooling cannot maintain safe gradient", "core cooling can't hold gradient"),
    ("transient disturbed auxiliary pump control", "transient hit aux pump ctrl"),
    ("indicates unstable refill trend", "unstable refill"),
    ("level estimate dropped near minimum reserve line", "level near min reserve"),
    ("reported repeated cavitation signatures", "repeated cavitation"),
    ("suction profile inconsistent with expected coolant volume", "suction inconsistent"),
    ("feedback loop exceeded correction budget", "feedback loop > corr"),
    ("return circuit temperature rose faster than prediction", "return temp rose fast"),
    ("fails to recover thermal margin while WTANK07 partially filled", "no thermal recovery, WTANK07 partial"),
    ("cannot remove heat with current WTANK07 volume", "can't remove heat, WTANK07 vol"),
    ("Cross-check between FIRMWARE and hardware interface map did not complete successfully", "FIRMWARE/HW map cross-check failed"),
    ("Safety bootstrap read missing environment marker", "Safety bootstrap missing"),
    ("entered critical protection state during startup", "crit protection at startup"),
    ("Operational fault persisted on", "Op fault on"),
    (" after retry cycle", ""),
    (" returned inconsistent feedback under load", " inconsistent under load"),
    ("Control response from", "Ctrl resp"),
    (" exceeded error budget", " > err budget"),
    (" highly unstable under startup load", " unstable at startup"),
    ("Power stability on", "Power stability"),
]


def _shorten(body: str, *, keep_two_sentences: bool = False) -> str:
    sentences = [s.strip() for s in body.split(".") if s.strip()]
    if not sentences:
        return body.strip()
    keep = sentences[:2] if keep_two_sentences else sentences[:1]
    text = ". ".join(keep) + "."
    for old, new in _PHRASE_SHORTENINGS:
        text = text.replace(old, new)
    for pattern, repl in _FILLER_RES:
        text = pattern.sub(repl, text)
    text = text.strip().rstrip(".")
    return text + "." if text else text


_COMPONENT_RE = re.compile(r"\b(ECCS\d*|WTRPMP|WTANK\d*|PWR\d*|STMTURB\d*|WSTPOOL\d*|FIRMWARE)\b")


def _line_components(body: str) -> set[str]:
    return set(_COMPONENT_RE.findall(body))


def algo_condense(
    filtered: str,
    *,
    target_chars: int = OUTPUT_CHAR_TARGET,
    keep_two_sentences: bool = False,
    drop_covered_warn: bool = True,
    rich_components: frozenset[str] | None = None,
) -> str:
    """Deterministic compression: one line per (level, first-sentence) signature.

    For each unique signature, emit a single line with the FIRST occurrence's
    timestamp (HH:MM, no seconds), shortened description, and a recurrence count.
    WARN lines are dropped if a CRIT/ERR exists for the same component — the
    higher-severity event already covers it for failure analysis.
    """
    @dataclass
    class Group:
        date: str
        first_hm: str
        last_hm: str
        level: str
        body: str
        count: int = 0

    groups: dict[tuple[str, str], Group] = {}
    for line in filtered.splitlines():
        m = _LINE_RE.match(line)
        if not m:
            continue
        date, hh, mm, _ss, level, body = m.groups()
        first_sent = body.split(".")[0].strip()
        key = (level, first_sent.lower())
        hm = f"{hh}:{mm}"
        if key not in groups:
            groups[key] = Group(date=date, first_hm=hm, last_hm=hm, level=level, body=body, count=1)
        else:
            g = groups[key]
            g.count += 1
            g.last_hm = hm  # filtered is sorted chronologically

    high_level = {"CRIT", "CRITICAL", "FATAL", "ALERT", "EMERG", "EMERGENCY", "ERR", "ERRO", "ERROR"}
    components_with_high: set[str] = set()
    for g in groups.values():
        if g.level in high_level:
            components_with_high.update(_line_components(g.body))

    rich = rich_components or frozenset()
    rendered: list[tuple[str, str, int, str]] = []  # (date, first_hm, importance, line)
    for g in groups.values():
        comps = _line_components(g.body)
        is_rich = bool(comps & rich)
        if drop_covered_warn and not is_rich and g.level not in high_level:
            if comps and comps.issubset(components_with_high):
                # Component already represented by a higher-severity event.
                continue
        # Components named in technician feedback get the longer two-sentence form.
        line_two = keep_two_sentences or is_rich
        short = _shorten(g.body, keep_two_sentences=line_two)
        suffix = f" x{g.count}" if g.count > 1 else ""
        line = f"[{g.date} {g.first_hm}] [{g.level}] {short}{suffix}"
        importance = 0 if g.level in high_level else 1
        rendered.append((g.date, g.first_hm, importance, line))

    rendered.sort(key=lambda t: (t[0], t[1]))
    out = "\n".join(line for _, _, _, line in rendered)

    # If still over budget, drop the longest remaining WARN lines first.
    if len(out) > target_chars:
        kept: list[str | None] = [line for _, _, _, line in rendered]
        warn_idx = [i for i, ln in enumerate(kept) if ln and "[WARN" in ln]
        warn_idx.sort(key=lambda i: -len(kept[i] or ""))
        for i in warn_idx:
            if len("\n".join(ln for ln in kept if ln)) <= target_chars:
                break
            kept[i] = None
        out = "\n".join(ln for ln in kept if ln)

    return out


def _components_from_feedback(feedback: str | None) -> frozenset[str]:
    if not feedback:
        return frozenset()
    return frozenset(_COMPONENT_RE.findall(feedback))


def condense(
    client: genai.Client | None,
    filtered: str,
    feedback: str | None,
    *,
    use_llm: bool = False,
) -> str:
    """Produce a condensed log; default path is algorithmic, LLM is opt-in."""
    if use_llm and client is not None:
        try:
            prompt = build_prompt(filtered, feedback)
            condensed = gemini_condense(client, prompt)
            chars = len(condensed)
            tokens = estimate_tokens(condensed)
            print(f"[condense] LLM initial: {chars:,} chars, ~{tokens:,} est. tokens")
            if chars <= OUTPUT_CHAR_HARD_CAP:
                CONDENSED_LOG.write_text(condensed, encoding="utf-8")
                return condensed
            print(f"[condense] LLM output over cap; falling back to algorithmic")
        except Exception as e:  # noqa: BLE001
            print(f"[condense] LLM unavailable ({type(e).__name__}); using algorithmic path")

    rich = _components_from_feedback(feedback)
    if rich:
        print(f"[condense] feedback flagged components: {sorted(rich)}")

    # Prefer the richer (two-sentence + keep all WARN for flagged components) form;
    # fall back to terser variants if the rich form blows the budget.
    candidates = [
        ("2-sent, drop covered WARN", dict(keep_two_sentences=True, drop_covered_warn=True)),
        ("2-sent, keep WARN", dict(keep_two_sentences=True, drop_covered_warn=False)),
        ("1-sent, keep WARN", dict(keep_two_sentences=False, drop_covered_warn=False)),
        ("1-sent, drop covered WARN", dict(keep_two_sentences=False, drop_covered_warn=True)),
    ]
    chosen: str | None = None
    for label, kwargs in candidates:
        candidate = algo_condense(
            filtered, target_chars=OUTPUT_CHAR_HARD_CAP, rich_components=rich, **kwargs
        )
        if len(candidate) <= OUTPUT_CHAR_HARD_CAP:
            chosen = candidate
            print(f"[condense] using variant: {label}")
            break
    if chosen is None:
        # Last resort: terser variant + truncation
        chosen = algo_condense(
            filtered, target_chars=OUTPUT_CHAR_HARD_CAP,
            keep_two_sentences=False, drop_covered_warn=True,
            rich_components=rich,
        )

    chars = len(chosen)
    tokens = estimate_tokens(chosen)
    print(f"[condense] algorithmic: {chars:,} chars, ~{tokens:,} est. tokens "
          f"({len(chosen.splitlines())} lines)")

    if chars > OUTPUT_CHAR_HARD_CAP:
        print(f"[condense] still {chars:,} chars; hard-truncating at line boundary")
        truncated_lines: list[str] = []
        running = 0
        for line in chosen.splitlines():
            if running + len(line) + 1 > OUTPUT_CHAR_HARD_CAP:
                break
            truncated_lines.append(line)
            running += len(line) + 1
        chosen = "\n".join(truncated_lines)

    CONDENSED_LOG.write_text(chosen, encoding="utf-8")
    return chosen


def append_history(entry: str) -> None:
    with HISTORY_FILE.open("a", encoding="utf-8") as fh:
        fh.write(entry)
        if not entry.endswith("\n"):
            fh.write("\n")
        fh.write("---\n")


def extract_feedback(response: dict) -> str | None:
    """Pull whatever technician hint Centrala returns into a single string."""
    parts: list[str] = []
    for key in ("message", "hint", "feedback", "details", "note"):
        value = response.get(key)
        if value:
            parts.append(f"{key}: {value}" if isinstance(value, str) else f"{key}: {json.dumps(value, ensure_ascii=False)}")
    if not parts:
        # Fall back to the whole response sans apikey-ish noise.
        parts.append(json.dumps(response, ensure_ascii=False))
    return "\n".join(parts) if parts else None


def has_flag(response: dict) -> str | None:
    text = json.dumps(response, ensure_ascii=False)
    m = FLAG_RE.search(text)
    return m.group(0) if m else None


def submit_with_handling(condensed: str) -> dict:
    try:
        return submit_answer(TASK_NAME, {"logs": condensed})
    except requests.HTTPError as e:
        # Centrala returns body with the rejection reason even on non-2xx.
        body = e.response.text if e.response is not None else str(e)
        try:
            return json.loads(body)
        except (ValueError, TypeError):
            return {"error": str(e), "raw": body}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", help="Re-download failure.log even if cached")
    parser.add_argument("--max-iters", type=int, default=5, help="Max submission iterations")
    parser.add_argument("--dry-run", action="store_true", help="Skip Centrala submission")
    parser.add_argument("--use-llm", action="store_true", help="Try Gemini before falling back to algorithmic compression")
    args = parser.parse_args()

    load_env()
    api_key = os.environ.get("CENTRALA_API_KEY")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("CENTRALA_API_KEY missing", file=sys.stderr)
        return 2
    if not gemini_key:
        print("GEMINI_API_KEY missing", file=sys.stderr)
        return 2

    raw = download_log(api_key, refresh=args.refresh)
    raw_lines = len(raw.splitlines())
    print(f"[raw] {raw_lines:,} lines, ~{estimate_tokens(raw):,} est. tokens")

    filtered = pre_filter(raw)
    if not filtered.strip():
        print("[filter] no severe lines found — aborting", file=sys.stderr)
        return 3

    client = genai.Client(api_key=gemini_key) if args.use_llm else None

    feedback: str | None = None
    last_response: dict | None = None
    for iteration in range(1, args.max_iters + 1):
        print(f"\n=== iteration {iteration} ===")
        condensed = condense(client, filtered, feedback, use_llm=args.use_llm)
        tokens = estimate_tokens(condensed)
        print(f"[final] {len(condensed.splitlines())} lines, "
              f"{len(condensed):,} chars, ~{tokens:,} est. tokens")

        if args.dry_run:
            print("[dry-run] skipping Centrala submission")
            return 0

        append_history(
            f"=== iteration {iteration} ===\n"
            f"feedback_in: {feedback or '(none)'}\n"
            f"submitted ({tokens} est. tokens, {len(condensed.splitlines())} lines):\n{condensed}"
        )

        response = submit_with_handling(condensed)
        last_response = response
        print(f"[centrala] {json.dumps(response, ensure_ascii=False, indent=2)}")
        append_history(f"response: {json.dumps(response, ensure_ascii=False)}")

        flag = has_flag(response)
        if flag:
            print(f"\nFLAG: {flag}")
            return 0

        new_feedback = extract_feedback(response)
        if not new_feedback:
            print("[centrala] no actionable feedback — stopping")
            break
        if new_feedback == feedback:
            print("[centrala] feedback unchanged — stopping to avoid loop")
            break
        feedback = new_feedback

        # Polite pause between submissions.
        time.sleep(2)

    print("\nNo flag captured.")
    if last_response is not None:
        print(json.dumps(last_response, ensure_ascii=False, indent=2))
    return 1


if __name__ == "__main__":
    sys.exit(main())
