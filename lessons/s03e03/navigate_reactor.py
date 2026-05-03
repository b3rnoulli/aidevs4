"""S03E03 — Navigate the cooling-module robot through the reactor grid.

The /verify API exposes a 7x5 grid where the robot starts at (col 1, row 5)
and must reach (col 7, row 5). Reactor blocks oscillate vertically and only
advance when a command is sent. Per turn we send one of:
    start, right, left, wait, reset
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import requests
from dotenv import load_dotenv

from aidevs4.centrala import submit_answer

LESSON_DIR = Path(__file__).resolve().parent
TRACE_FILE = LESSON_DIR / "navigate_trace.txt"

TASK_NAME = "reactor"
ROWS = 5
COLS = 7
START_ROW = 5
START_COL = 1
GOAL_ROW = 5
GOAL_COL = 7

FLAG_RE = re.compile(r"\{FLG:[^}]+\}")


@dataclass(frozen=True)
class Block:
    col: int
    top_row: int
    bottom_row: int
    direction: str  # "up" or "down"

    def cells(self) -> set[tuple[int, int]]:
        return {(self.col, r) for r in range(self.top_row, self.bottom_row + 1)}


def load_env() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    load_dotenv(repo_root / ".env")
    load_dotenv(repo_root.parent.parent.parent / ".env")


def parse_blocks(payload: dict) -> list[Block]:
    return [
        Block(
            col=int(b["col"]),
            top_row=int(b["top_row"]),
            bottom_row=int(b["bottom_row"]),
            direction=str(b["direction"]),
        )
        for b in payload.get("blocks", [])
    ]


def advance_block(b: Block) -> Block:
    """One tick of the block oscillation. Direction flips at the extremes."""
    delta = 1 if b.direction == "down" else -1
    new_top = b.top_row + delta
    new_bottom = b.bottom_row + delta
    new_dir = b.direction
    if new_top == 1 and delta == -1:
        new_dir = "down"
    elif new_bottom == ROWS and delta == 1:
        new_dir = "up"
    return Block(col=b.col, top_row=new_top, bottom_row=new_bottom, direction=new_dir)


def occupied_cells(blocks: list[Block]) -> set[tuple[int, int]]:
    cells: set[tuple[int, int]] = set()
    for b in blocks:
        cells |= b.cells()
    return cells


def is_safe(player_col: int, player_row: int, blocks: list[Block]) -> bool:
    return (player_col, player_row) not in occupied_cells(blocks)


def render_board(player_col: int, player_row: int, blocks: list[Block]) -> str:
    grid = [["." for _ in range(COLS)] for _ in range(ROWS)]
    for col, row in occupied_cells(blocks):
        if 1 <= row <= ROWS and 1 <= col <= COLS:
            grid[row - 1][col - 1] = "B"
    if 1 <= player_row <= ROWS and 1 <= player_col <= COLS:
        grid[player_row - 1][player_col - 1] = "P"
    if 1 <= GOAL_ROW <= ROWS and 1 <= GOAL_COL <= COLS:
        if grid[GOAL_ROW - 1][GOAL_COL - 1] == ".":
            grid[GOAL_ROW - 1][GOAL_COL - 1] = "G"
    return "\n".join(" ".join(row) for row in grid)


def advance_blocks(blocks: list[Block]) -> list[Block]:
    return [advance_block(b) for b in blocks]


def plan_path(
    player_col: int,
    player_row: int,
    blocks: list[Block],
    *,
    max_steps: int = 60,
) -> list[str] | None:
    """BFS over (player_col, tick) until the robot reaches the goal column.

    Block configuration after k ticks is fully determined by repeatedly applying
    advance_block, so we cache it per tick to keep the search cheap.
    """
    block_states: list[list[Block]] = [blocks]

    def blocks_at(tick: int) -> list[Block]:
        while len(block_states) <= tick:
            block_states.append(advance_blocks(block_states[-1]))
        return block_states[tick]

    # State: (player_col, tick). player_row is always 5.
    start = (player_col, 0)
    if (player_col, player_row) in occupied_cells(blocks_at(0)):
        return None  # already dead

    queue: list[tuple[tuple[int, int], list[str]]] = [(start, [])]
    visited: set[tuple[int, int]] = {start}

    moves: list[tuple[str, int]] = [
        ("right", +1),
        ("wait", 0),
        ("left", -1),
    ]

    while queue:
        (col, tick), path = queue.pop(0)
        if col == GOAL_COL:
            return path
        if len(path) >= max_steps:
            continue
        next_tick = tick + 1
        nb = blocks_at(next_tick)
        nb_cells = occupied_cells(nb)
        for cmd, delta in moves:
            new_col = col + delta
            if not (1 <= new_col <= COLS):
                continue
            if (new_col, player_row) in nb_cells:
                continue
            state = (new_col, next_tick % 6)
            if state in visited:
                continue
            visited.add(state)
            queue.append(((new_col, next_tick), path + [cmd]))

    return None


def choose_command(player_col: int, player_row: int, blocks: list[Block]) -> str:
    """Plan a full safe path and return the first command. Falls back to wait."""
    path = plan_path(player_col, player_row, blocks)
    if not path:
        # No path found — wait and replan next turn (the board will look
        # different one tick later).
        return "wait"
    return path[0]


def trace(text: str) -> None:
    print(text)
    with TRACE_FILE.open("a", encoding="utf-8") as fh:
        fh.write(text + "\n")


def submit_with_handling(command: str) -> dict:
    try:
        return submit_answer(TASK_NAME, {"command": command})
    except requests.HTTPError as e:
        body = e.response.text if e.response is not None else str(e)
        try:
            return json.loads(body)
        except (ValueError, TypeError):
            return {"error": str(e), "raw": body}


def has_flag(payload: dict) -> str | None:
    text = json.dumps(payload, ensure_ascii=False)
    m = FLAG_RE.search(text)
    return m.group(0) if m else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-steps", type=int, default=200,
                        help="Safety cap on the number of commands sent")
    parser.add_argument("--reset-first", action="store_true",
                        help="Send a reset before starting (in case a session is open)")
    args = parser.parse_args()

    load_env()
    if not os.environ.get("CENTRALA_API_KEY"):
        print("CENTRALA_API_KEY missing", file=sys.stderr)
        return 2

    TRACE_FILE.write_text("", encoding="utf-8")  # truncate

    if args.reset_first:
        trace("[reset]")
        trace(json.dumps(submit_with_handling("reset"), ensure_ascii=False))

    trace("[start]")
    state = submit_with_handling("start")
    trace(json.dumps(state, ensure_ascii=False))

    for step in range(1, args.max_steps + 1):
        if state.get("reached_goal"):
            break
        flag = has_flag(state)
        if flag:
            trace(f"\nFLAG: {flag}")
            return 0
        if "player" not in state or "blocks" not in state:
            trace(f"[stop] unexpected state shape: {state}")
            return 1

        player = state["player"]
        player_col, player_row = int(player["col"]), int(player["row"])
        blocks = parse_blocks(state)

        trace(f"\n--- step {step} ---")
        trace(f"player=({player_col},{player_row})  goal=({GOAL_COL},{GOAL_ROW})")
        trace(render_board(player_col, player_row, blocks))

        cmd = choose_command(player_col, player_row, blocks)
        trace(f"-> {cmd}")
        state = submit_with_handling(cmd)
        trace(json.dumps(state, ensure_ascii=False))
        time.sleep(0.2)  # gentle pacing

    flag = has_flag(state)
    if flag:
        trace(f"\nFLAG: {flag}")
        return 0

    if state.get("reached_goal"):
        trace("\nReached goal but no flag in payload — full last response above.")
        return 0

    trace("\nDid not reach goal within step cap.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
