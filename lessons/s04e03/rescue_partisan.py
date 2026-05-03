"""S04E03 — Domatowo rescue: locate the partisan hiding in one of the
3-storey blocks (B3) and call the helicopter to that cell.

Plan:
1. reset, fetch map.
2. Find every B3 cell, group into 3 clusters (top-right, bottom-left, bottom-right).
3. Spawn one transporter carrying 3 scouts (5 + 3*5 = 20 AP).
4. Drive to a road tile next to each cluster, dismount one scout per cluster.
5. Walk each scout through every B3 cell of its cluster, inspecting each.
   After every inspect, read getLogs and look for a "human found" hit.
6. When a scout reports the partisan, call callHelicopter at that cell.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import requests
from dotenv import load_dotenv

from aidevs4.centrala import submit_answer

LESSON_DIR = Path(__file__).resolve().parent
MAP_CACHE = LESSON_DIR / "map.json"
TRACE_FILE = LESSON_DIR / "rescue_trace.txt"

TASK_NAME = "domatowo"
FLAG_RE = re.compile(r"\{FLG:[^}]+\}")

# Negative inspect responses observed so far all open with one of these markers.
# Anything *not* matching this AND matching a positive marker is a likely hit.
NEGATIVE_RE = re.compile(
    r"\b(brak|nikt|nikogo|niko[ms]|pust[oyaie]?|żadn|martw|opusz)\b"
    r"|nie\s+(natrafi|odnalezi|znala|wykry|widz|spotka|ma\s+nikogo)"
    r"|^nie\s",
    re.IGNORECASE,
)
POSITIVE_RE = re.compile(
    r"człowiek|partyzant|widz[ęeę]|ranny|przeży|pomocy|spotka[lłn]|"
    r"kontakt nawiąz|znaleziono\s+(człowieka|partyzanta|kogo|osob)|"
    r"\bznalaz[lłn]em\b|\bjest\s+tu\b|\bzywy\b|\bżywy\b",
    re.IGNORECASE,
)


def load_env() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    load_dotenv(repo_root / ".env")
    load_dotenv(repo_root.parent.parent.parent / ".env")


def trace(text: str) -> None:
    print(text)
    with TRACE_FILE.open("a", encoding="utf-8") as fh:
        fh.write(text + "\n")


def call(action: str, **kw) -> dict:
    payload: dict = {"action": action, **kw}
    trace(f">>> {json.dumps(payload, ensure_ascii=False)}")
    try:
        resp = submit_answer(TASK_NAME, payload)
    except requests.HTTPError as e:
        body = e.response.text if e.response is not None else str(e)
        trace(f"<<< HTTP error: {body}")
        raise
    trace(f"<<< {json.dumps(resp, ensure_ascii=False)}")
    return resp


def coord_to_rc(coord: str) -> tuple[int, int]:
    """A1..K11 -> (row 0-indexed, col 0-indexed)."""
    col = ord(coord[0].upper()) - ord("A")
    row = int(coord[1:]) - 1
    return row, col


def rc_to_coord(row: int, col: int) -> str:
    return f"{chr(ord('A') + col)}{row + 1}"


def fetch_map() -> dict:
    if MAP_CACHE.exists():
        return json.loads(MAP_CACHE.read_text(encoding="utf-8"))
    resp = call("getMap")
    if "map" in resp:
        MAP_CACHE.write_text(json.dumps(resp["map"], indent=2, ensure_ascii=False),
                             encoding="utf-8")
        return resp["map"]
    raise RuntimeError(f"unexpected getMap response: {resp}")


def cluster_b3_cells(grid: list[list[str]]) -> list[list[str]]:
    """Group all B3 cells into connected clusters (4-neighbour connectivity)."""
    n = len(grid)
    seen: set[tuple[int, int]] = set()
    clusters: list[list[str]] = []
    for r in range(n):
        for c in range(n):
            if grid[r][c] != "block3" or (r, c) in seen:
                continue
            stack = [(r, c)]
            cells: list[tuple[int, int]] = []
            while stack:
                rr, cc = stack.pop()
                if (rr, cc) in seen:
                    continue
                if not (0 <= rr < n and 0 <= cc < n) or grid[rr][cc] != "block3":
                    continue
                seen.add((rr, cc))
                cells.append((rr, cc))
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    stack.append((rr + dr, cc + dc))
            clusters.append([rc_to_coord(rr, cc) for rr, cc in cells])
    return clusters


def adjacent_road_for(cluster: list[str], grid: list[list[str]]) -> str:
    """Pick a road tile adjacent to any cell of the cluster (closest to spawn row 6)."""
    n = len(grid)
    candidates: list[tuple[int, str]] = []
    for cell in cluster:
        r, c = coord_to_rc(cell)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            rr, cc = r + dr, c + dc
            if 0 <= rr < n and 0 <= cc < n and grid[rr][cc] == "road":
                # Prefer road tiles closer to row 6 (transporter starting hub).
                dist_to_hub = abs(rr - 5)
                candidates.append((dist_to_hub, rc_to_coord(rr, cc)))
    if not candidates:
        raise RuntimeError(f"no adjacent road for cluster {cluster}")
    candidates.sort()
    return candidates[0][1]


def order_inspections(cluster: list[str], entry_road: str, grid: list[list[str]]) -> list[str]:
    """Order B3 cells by walking distance from the dismount road tile."""
    er, ec = coord_to_rc(entry_road)
    def dist(cell: str) -> int:
        cr, cc = coord_to_rc(cell)
        return abs(cr - er) + abs(cc - ec)
    return sorted(cluster, key=dist)


def get_position(unit_id: str) -> str:
    resp = call("getObjects")
    for o in resp.get("objects", []):
        if o["id"] == unit_id:
            return o["position"]
    raise RuntimeError(f"unit {unit_id} not in getObjects")


def latest_log_for(scout_id: str) -> dict | None:
    resp = call("getLogs")
    for entry in reversed(resp.get("logs", [])):
        if entry.get("scout") == scout_id:
            return entry
    return None


def is_negative(msg: str) -> bool:
    return bool(NEGATIVE_RE.search(msg))


def is_positive(msg: str) -> bool:
    return bool(POSITIVE_RE.search(msg))


def classify_with_gemini(messages: list[tuple[str, str]]) -> str | None:
    """Ask Gemini which cell's message implies the partisan is there.

    Used only when regex heuristics are inconclusive.
    """
    try:
        from google import genai
        from google.genai import types
    except Exception:
        return None
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None

    client = genai.Client(api_key=api_key)
    listing = "\n".join(f"{cell}: {msg}" for cell, msg in messages)
    prompt = (
        "Each line below is a Polish reconnaissance log from a scout inspecting "
        "a tile in a ruined town. Exactly one of them indicates the scout has "
        "FOUND a wounded partisan hiding there (audio context: 'Mam broń, jestem "
        "ranny. Ukryłem się w jednym z najwyższych bloków. Nie mam jedzenia. "
        "Pomocy.'). All other lines describe NO contact, empty rooms, debris.\n\n"
        f"{listing}\n\n"
        "Reply with ONLY the coordinate (e.g. F1) of the line that indicates a found human."
    )
    for model in ("gemini-2.5-flash-lite", "gemini-2.5-flash", "gemini-2.0-flash"):
        try:
            resp = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="text/plain",
                    temperature=0.0,
                ),
            )
            text = (resp.text or "").strip().upper()
            m = re.match(r"([A-K]\d{1,2})", text)
            if m:
                return m.group(1)
        except Exception as e:
            trace(f"[gemini] {model} failed: {e}")
    return None


@dataclass
class MissionState:
    grid: list[list[str]]
    clusters: list[list[str]]
    cluster_entry: dict[int, str] = field(default_factory=dict)


def plan_mission(map_data: dict) -> MissionState:
    grid = map_data["grid"]
    clusters = cluster_b3_cells(grid)
    state = MissionState(grid=grid, clusters=clusters)
    for i, cluster in enumerate(clusters):
        state.cluster_entry[i] = adjacent_road_for(cluster, grid)
    return state


def execute_mission(state: MissionState) -> str | None:
    # Reset to ensure full action point budget.
    call("reset")

    n_clusters = len(state.clusters)
    transporter_resp = call("create", type="transporter", passengers=n_clusters)
    transporter_id = transporter_resp["object"]
    crew_ids = [c["id"] for c in transporter_resp.get("crew", []) if c["role"] == "scout"]
    if len(crew_ids) < n_clusters:
        raise RuntimeError(f"transporter only has {len(crew_ids)} scouts; need {n_clusters}")
    trace(f"[plan] {n_clusters} clusters: {state.clusters}")
    trace(f"[plan] entries: {state.cluster_entry}")

    # Drop one scout at each cluster's entry road.
    cluster_to_scout: dict[int, str] = {}
    for i, cluster in enumerate(state.clusters):
        entry = state.cluster_entry[i]
        call("move", object=transporter_id, where=entry)
        # Confirm transporter arrived (it should — path is auto-routed).
        time.sleep(0.2)
        call("dismount", object=transporter_id, passengers=1)
        # The dismounted scout should appear near the transporter; map it via getObjects.
        objs = call("getObjects")
        positioned = {o["id"]: o["position"] for o in objs.get("objects", [])}
        # Pick a scout id that hasn't been assigned yet AND is near the entry.
        er, ec = coord_to_rc(entry)
        unassigned = [sid for sid in crew_ids if sid in positioned and sid not in cluster_to_scout.values()]
        # pick the closest one to entry (in case the API reordered)
        unassigned.sort(key=lambda sid: abs(coord_to_rc(positioned[sid])[0] - er) + abs(coord_to_rc(positioned[sid])[1] - ec))
        if not unassigned:
            # Some installations spawn a fresh scout id on dismount; refresh from getObjects.
            scout_obj = next((o for o in objs.get("objects", []) if o["typ"] == "scout"
                              and o["id"] not in cluster_to_scout.values()), None)
            if scout_obj is None:
                raise RuntimeError("no scout available after dismount")
            cluster_to_scout[i] = scout_obj["id"]
        else:
            cluster_to_scout[i] = unassigned[0]
        trace(f"[plan] cluster {i} -> entry {entry} -> scout {cluster_to_scout[i]}")

    # Walk each scout through its cluster's B3 cells, inspecting each. We
    # collect every (cell, msg) and decide AFTER the sweep — single false-
    # positive regex hits cost the mission, so we err on the side of completeness.
    collected: list[tuple[str, str]] = []
    confident_hit: str | None = None
    for i, cluster in enumerate(state.clusters):
        if confident_hit:
            break
        entry = state.cluster_entry[i]
        scout_id = cluster_to_scout[i]
        order = order_inspections(cluster, entry, state.grid)
        trace(f"\n[scout {i}] inspecting {order} from entry {entry}")
        for cell in order:
            try:
                call("move", object=scout_id, where=cell)
            except requests.HTTPError as e:
                trace(f"[scout {i}] move to {cell} failed: {e}; trying inspect from current cell")
            time.sleep(0.2)
            call("inspect", object=scout_id)
            log = latest_log_for(scout_id)
            if log is None:
                trace(f"[scout {i}] no log entry returned; continuing")
                continue
            field_at = log.get("field")
            msg = log.get("msg", "")
            trace(f"[scout {i}] log @ {field_at}: {msg}")
            collected.append((field_at, msg))
            # Strong-confidence early stop: positive markers and no negation.
            if is_positive(msg) and not is_negative(msg):
                confident_hit = field_at
                trace(f"\n*** confident partisan hit at {field_at}: {msg} ***")
                break

    if confident_hit:
        return confident_hit

    # No confident regex match — pick the message that is the most "outlier"
    # vs. the negative ones. First retry: any positive marker, regardless of
    # negation overlap. Then: ask Gemini.
    positives = [(c, m) for c, m in collected if is_positive(m)]
    if len(positives) == 1:
        trace(f"[fallback] unique positive marker hit at {positives[0][0]}")
        return positives[0][0]
    if len(positives) > 1:
        trace(f"[fallback] multiple positives: {positives}; asking Gemini")
    else:
        trace("[fallback] no positives; asking Gemini")

    cell = classify_with_gemini(collected)
    if cell:
        trace(f"[gemini] picked {cell}")
        return cell
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-call", action="store_true",
                        help="Find the partisan but skip the helicopter call (debug)")
    args = parser.parse_args()

    load_env()
    if not os.environ.get("CENTRALA_API_KEY"):
        print("CENTRALA_API_KEY missing", file=sys.stderr)
        return 2

    TRACE_FILE.write_text("", encoding="utf-8")  # truncate

    map_data = fetch_map()
    state = plan_mission(map_data)
    found_at = execute_mission(state)

    if not found_at:
        trace("\nDid not locate partisan. Inspect the trace for diagnostics.")
        return 1

    if args.no_call:
        trace(f"\n[--no-call] would call helicopter to {found_at}")
        return 0

    resp = call("callHelicopter", destination=found_at)
    flag_match = FLAG_RE.search(json.dumps(resp, ensure_ascii=False))
    if flag_match:
        trace(f"\nFLAG: {flag_match.group(0)}")
        return 0

    trace(f"\nHelicopter call returned: {resp}")
    return 0 if resp.get("code", -1) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
