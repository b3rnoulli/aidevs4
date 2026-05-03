"""Solves the S02E02 `electricity` puzzle.

Algorithm:
1. Download current and target board PNGs.
2. Detect each board's grid bounding box from dark-pixel projections.
3. Crop into a 3x3 cell grid and infer which edges (top/right/bottom/left)
   have a cable connection by sampling a small inset band at each edge midpoint.
4. For each cell, compute the minimum number of 90-degree clockwise rotations
   that transform the current edge-set into the target edge-set.
5. POST one rotation per request to https://hub.ag3nts.org/verify until done.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv
from PIL import Image

from aidevs4.centrala import submit_answer

CACHE_DIR = Path(__file__).parent / "cache"
TASK_NAME = "electricity"
TARGET_URL = "https://hub.ag3nts.org/i/solved_electricity.png"

Sides = tuple[bool, bool, bool, bool]  # (top, right, bottom, left)


def board_url(api_key: str, reset: bool = False) -> str:
    qs = "?reset=1" if reset else ""
    return f"https://hub.ag3nts.org/data/{api_key}/electricity.png{qs}"


def download(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    dest.write_bytes(response.content)
    return dest


def find_grid_bbox(path: Path) -> tuple[int, int, int, int]:
    """Find the grid square via dark-pixel column/row projections.

    The grid's vertical lines have very dense dark columns; horizontal lines
    are slightly less dense (cables interrupt them) so we use a lower
    threshold for rows.
    """
    img = Image.open(path).convert("L")
    w, h = img.size
    px = img.load()
    dark_threshold = 80
    col_counts = [0] * w
    row_counts = [0] * h
    for y in range(h):
        for x in range(w):
            if px[x, y] < dark_threshold:
                col_counts[x] += 1
                row_counts[y] += 1
    vlines = [x for x in range(w) if col_counts[x] > h * 0.4]
    hlines = [y for y in range(h) if row_counts[y] > w * 0.25]
    if not vlines or not hlines:
        raise RuntimeError(f"Could not detect grid in {path}")
    return vlines[0], hlines[0], vlines[-1], hlines[-1]


def parse_cell_sides(path: Path) -> dict[tuple[int, int], Sides]:
    """Return {(row, col): (top, right, bottom, left)} for each of the 9 cells."""
    img = Image.open(path).convert("L")
    x0, y0, x1, y1 = find_grid_bbox(path)
    cw = (x1 - x0) / 3
    ch = (y1 - y0) / 3

    band = 6        # half-width of midpoint sample band (pixels each side of center)
    depth_outer = 4  # skip the very outer line (could be grid border)
    depth_inner = 18  # how far inward we sample
    dark_threshold = 100
    side_threshold = 0.25  # min ratio of dark pixels in band to count as a connection

    sides: dict[tuple[int, int], Sides] = {}
    for r in range(3):
        for c in range(3):
            cell = img.crop((
                int(x0 + c * cw), int(y0 + r * ch),
                int(x0 + (c + 1) * cw), int(y0 + (r + 1) * ch),
            ))
            cw_i, ch_i = cell.size
            mid_x, mid_y = cw_i // 2, ch_i // 2
            px = cell.load()

            def ratio(xs: range, ys: range) -> float:
                cnt = total = 0
                for y in ys:
                    if y < 0 or y >= ch_i:
                        continue
                    for x in xs:
                        if x < 0 or x >= cw_i:
                            continue
                        total += 1
                        if px[x, y] < dark_threshold:
                            cnt += 1
                return cnt / total if total else 0.0

            top = ratio(range(mid_x - band, mid_x + band + 1),
                        range(depth_outer, depth_inner)) > side_threshold
            bottom = ratio(range(mid_x - band, mid_x + band + 1),
                           range(ch_i - depth_inner, ch_i - depth_outer)) > side_threshold
            left = ratio(range(depth_outer, depth_inner),
                         range(mid_y - band, mid_y + band + 1)) > side_threshold
            right = ratio(range(cw_i - depth_inner, cw_i - depth_outer),
                          range(mid_y - band, mid_y + band + 1)) > side_threshold

            sides[(r + 1, c + 1)] = (top, right, bottom, left)
    return sides


def rotate_cw(state: Sides) -> Sides:
    """A 90 deg CW rotation maps top->right, right->bottom, bottom->left, left->top."""
    t, r, b, l = state
    return (l, t, r, b)


def rotations_to_match(curr: Sides, tgt: Sides) -> int | None:
    s = curr
    for k in range(4):
        if s == tgt:
            return k
        s = rotate_cw(s)
    return None


def fmt(state: Sides) -> str:
    t, r, b, l = state
    flags = []
    if t: flags.append("T")
    if r: flags.append("R")
    if b: flags.append("B")
    if l: flags.append("L")
    return "+".join(flags) if flags else "·"


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true",
                        help="Hit ?reset=1 on the board image before solving")
    parser.add_argument("--dry-run", action="store_true",
                        help="Compute rotation plan but do not POST any rotations")
    args = parser.parse_args()

    api_key = os.environ["CENTRALA_API_KEY"]

    target_path = CACHE_DIR / "electricity_target.png"
    current_path = CACHE_DIR / "electricity_current.png"

    print(f"[fetch] target -> {TARGET_URL}")
    download(TARGET_URL, target_path)

    print(f"[fetch] current{' (reset)' if args.reset else ''}")
    download(board_url(api_key, reset=args.reset), current_path)

    target = parse_cell_sides(target_path)
    current = parse_cell_sides(current_path)

    print("\n[parse] target:")
    for r in range(1, 4):
        print("  " + " | ".join(f"{r}x{c}={fmt(target[(r, c)]):>7}" for c in range(1, 4)))
    print("\n[parse] current:")
    for r in range(1, 4):
        print("  " + " | ".join(f"{r}x{c}={fmt(current[(r, c)]):>7}" for c in range(1, 4)))

    plan: list[tuple[int, int, int]] = []
    for (r, c), tgt in target.items():
        n = rotations_to_match(current[(r, c)], tgt)
        if n is None:
            print(f"\n[error] cell {r}x{c}: no rotation maps {fmt(current[(r,c)])} -> {fmt(tgt)}")
            print("  Detection probably misread one of the cells.")
            return 2
        if n:
            plan.append((r, c, n))

    total_rotations = sum(n for _, _, n in plan)
    print(f"\n[plan] {len(plan)} cells, {total_rotations} rotations:")
    for r, c, n in plan:
        print(f"  {r}x{c}: {n}x CW  ({fmt(current[(r,c)])} -> {fmt(target[(r,c)])})")

    if args.dry_run:
        print("\n[dry-run] not sending rotations.")
        return 0

    if not plan:
        print("\n[done] board already matches target — re-fetching to check for flag.")
    else:
        print("\n[apply] sending rotations...")

    last_response: dict | None = None
    for r, c, n in plan:
        cell = f"{r}x{c}"
        for i in range(n):
            print(f"  POST rotate {cell} ({i+1}/{n})")
            try:
                last_response = submit_answer(TASK_NAME, {"rotate": cell})
            except requests.HTTPError as exc:
                print(f"  HTTP error: {exc}")
                if exc.response is not None:
                    print("  Response body:", exc.response.text)
                return 1
            print(f"    -> {json.dumps(last_response, ensure_ascii=False)}")
            time.sleep(0.2)

    print("\n[final response]:")
    print(json.dumps(last_response, ensure_ascii=False, indent=2) if last_response else "(no rotations sent)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
