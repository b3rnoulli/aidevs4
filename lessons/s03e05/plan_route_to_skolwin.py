"""Solve task 'savethem': plan a route to Skolwin and submit it to /verify.

Discovers tools via /api/toolsearch (only 'maps' and 'wehicles' exist),
fetches the 10x10 Skolwin map and all four vehicles' specs, runs a
state-space search that lets the messenger dismount mid-trip to walk through
water tiles, then submits the cheapest plan.

The submission is an array starting with the chosen vehicle, with the literal
token "dismount" inserted to switch to walking. Vehicle-only mode and walk
modes alone cannot reach the goal within 10 fuel + 10 food on this map; a
mixed plan is required.
"""

from __future__ import annotations

import argparse
import heapq
import json
import os
import sys
import time
from collections import deque
from pathlib import Path

import requests
from dotenv import load_dotenv

from aidevs4.centrala import submit_answer

TASK = "savethem"
TOOLSEARCH_URL = "https://hub.ag3nts.org/api/toolsearch"
HUB_BASE = "https://hub.ag3nts.org"
MAP_QUERY = "Skolwin"
VEHICLE_NAMES = ("rocket", "horse", "walk", "car")
DIRECTIONS = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}
START_FUEL = 10.0
START_FOOD = 10.0
PASSABLE_TERRAIN_BY_VEHICLE = {
    "walk": {".", "S", "G", "W"},  # wading is allowed; T and R block
    "horse": {".", "S", "G", "W"},
    "rocket": {".", "S", "G"},  # cannot cross W
    "car": {".", "S", "G"},  # cannot cross W
}
LESSON_DIR = Path(__file__).parent
DISCOVERY_QUERIES = [
    "map of terrain",
    "vehicles and transport options",
    "rules and limits",
    "how to move",
    "starting equipment",
]


def _load_env() -> None:
    here = Path(__file__).resolve()
    for path in (here.parents[2] / ".env", here.parents[5] / ".env"):
        if path.exists():
            load_dotenv(path)
    if not os.environ.get("CENTRALA_API_KEY"):
        print("CENTRALA_API_KEY missing", file=sys.stderr)
        sys.exit(2)


def _post(url: str, payload: dict, *, retries: int = 5) -> dict:
    for attempt in range(retries):
        response = requests.post(url, json=payload, timeout=30)
        try:
            data = response.json()
        except ValueError:
            response.raise_for_status()
            raise
        if data.get("code") == -9999:
            wait = 8 * (attempt + 1)
            print(f"[rate-limit] {url} — sleeping {wait}s", file=sys.stderr)
            time.sleep(wait)
            continue
        return data
    raise RuntimeError(f"{url} kept rate-limiting after {retries} retries")


def discover_tools(api_key: str) -> dict[str, str]:
    """Use /api/toolsearch with a few seed queries; collect unique tools."""
    found: dict[str, str] = {}
    for query in DISCOVERY_QUERIES:
        data = _post(TOOLSEARCH_URL, {"apikey": api_key, "query": query})
        for tool in data.get("tools", []):
            found.setdefault(tool["name"], tool["url"])
    print(f"[discovery] tools: {found}")
    return found


def fetch_map(api_key: str, tool_url: str) -> tuple[list[list[str]], tuple[int, int], tuple[int, int]]:
    data = _post(f"{HUB_BASE}{tool_url}", {"apikey": api_key, "query": MAP_QUERY})
    if data.get("code") != 241:
        raise RuntimeError(f"unexpected maps response: {data}")
    grid = [list(row) for row in data["map"]]
    start = goal = None
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "S":
                start = (r, c)
            if cell == "G":
                goal = (r, c)
    if start is None or goal is None:
        raise RuntimeError("map missing S or G")
    print(f"[map] {data['cityName']} {len(grid)}x{len(grid[0])}, S={start}, G={goal}")
    return grid, start, goal


def fetch_vehicles(api_key: str, tool_url: str) -> dict[str, dict]:
    """Each query returns one vehicle; throttle to dodge rate-limits."""
    vehicles: dict[str, dict] = {}
    for name in VEHICLE_NAMES:
        data = _post(f"{HUB_BASE}{tool_url}", {"apikey": api_key, "query": name})
        if data.get("code") != 230:
            raise RuntimeError(f"unexpected vehicle response for {name!r}: {data}")
        vehicles[name] = {"fuel": float(data["consumption"]["fuel"]),
                          "food": float(data["consumption"]["food"])}
        time.sleep(8)
    print(f"[vehicles] {vehicles}")
    return vehicles


def plan_route(
    grid: list[list[str]],
    start: tuple[int, int],
    goal: tuple[int, int],
    vehicles: dict[str, dict],
) -> tuple[str, list[str]]:
    """Search for the cheapest reachable plan over (pos, fuel, food, mode).

    Mode is the active travel mode for cost accounting. Initial mode is the
    chosen starting vehicle; once dismounted the mode becomes 'walk' and stays
    there. Cost = fuel_used*1e3 + food_used (fuel is the binding resource on
    this map; tie-break on food).
    """
    H, W = len(grid), len(grid[0])
    best: tuple[str, list[str]] | None = None
    best_cost: float | None = None

    for starting in ("rocket", "horse", "car", "walk"):
        # state key includes quantized resource usage so Pareto-incomparable
        # states (e.g. cheap fuel but high food) aren't wrongly pruned.
        pq: list[tuple[float, float, float, int, int, str, bool, list[str]]] = []
        heapq.heappush(pq, (0.0, 0.0, 0.0, *start, starting, starting == "walk", [starting]))
        seen: dict[tuple[int, int, str, bool, int, int], float] = {}

        while pq:
            cost, fuel_used, food_used, r, c, mode, dismounted, path = heapq.heappop(pq)
            key = (r, c, mode, dismounted, round(fuel_used * 10), round(food_used * 10))
            if key in seen and seen[key] <= cost:
                continue
            seen[key] = cost
            if (r, c) == goal:
                if best_cost is None or cost < best_cost:
                    best_cost = cost
                    best = (starting, path[1:])
                break
            if not dismounted and mode != "walk":
                heapq.heappush(
                    pq,
                    (cost, fuel_used, food_used, r, c, "walk", True, path + ["dismount"]),
                )
            spec = vehicles[mode]
            new_fuel = fuel_used + spec["fuel"]
            new_food = food_used + spec["food"]
            if new_fuel > START_FUEL or new_food > START_FOOD:
                continue
            for direction, (dr, dc) in DIRECTIONS.items():
                nr, nc = r + dr, c + dc
                if not (0 <= nr < H and 0 <= nc < W):
                    continue
                if grid[nr][nc] not in PASSABLE_TERRAIN_BY_VEHICLE[mode]:
                    continue
                step_cost = spec["fuel"] * 1000.0 + spec["food"]
                heapq.heappush(
                    pq,
                    (
                        cost + step_cost,
                        new_fuel,
                        new_food,
                        nr,
                        nc,
                        mode,
                        dismounted,
                        path + [direction],
                    ),
                )

    if best is None:
        raise RuntimeError("no feasible plan within fuel/food budget")
    return best


def find_flag(response: dict) -> str | None:
    text = json.dumps(response, ensure_ascii=False)
    import re
    match = re.search(r"\{FLG:[^}]+\}", text)
    return match.group(0) if match else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan and submit a route to Skolwin.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Plan and print the answer, but do not POST to /verify.")
    args = parser.parse_args()

    _load_env()
    api_key = os.environ["CENTRALA_API_KEY"]

    tools = discover_tools(api_key)
    if "maps" not in tools or "wehicles" not in tools:
        print(f"missing required tools, found: {tools}", file=sys.stderr)
        return 1

    grid, start, goal = fetch_map(api_key, tools["maps"])
    vehicles = fetch_vehicles(api_key, tools["wehicles"])

    starting_vehicle, plan_tail = plan_route(grid, start, goal, vehicles)
    answer = [starting_vehicle, *plan_tail]
    print(f"[plan] starting vehicle: {starting_vehicle}")
    print(f"[plan] {len(plan_tail)} tokens: {plan_tail}")
    print(f"[answer] {json.dumps(answer)}")

    if args.dry_run:
        print("[dry-run] not submitting")
        return 0

    response = submit_answer(TASK, answer)
    print(json.dumps(response, ensure_ascii=False, indent=2))
    flag = find_flag(response)
    if flag:
        print(f"\nFLAG: {flag}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
