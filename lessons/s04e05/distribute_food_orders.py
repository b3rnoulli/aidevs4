"""Solve task 'foodwarehouse': create one warehouse order per city in
food4cities.json so all city needs are satisfied, then call 'done'.

The API tools live behind a single /verify endpoint:
  - help: documentation
  - database: read-only SQLite (destinations, users, roles)
  - signatureGenerator: SHA1 signature for (login, birthday, destination)
  - orders: get/create/append/delete
  - reset: restore initial state (4 seed orders for unrelated cities)
  - done: validate the final order set and return the flag

Strategy: reset, delete the seed orders so the state contains only our 8 city
orders, look up each destination_id in the database, generate a fresh
signature per (creator, destination), create + populate one order per city
exactly matching food4cities.json quantities, then submit 'done'.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

TASK = "foodwarehouse"
VERIFY_URL = "https://hub.ag3nts.org/verify"
NEEDS_URL = "https://hub.ag3nts.org/dane/food4cities.json"
LESSON_DIR = Path(__file__).parent
NEEDS_PATH = LESSON_DIR / "food4cities.json"
FLAG_RE = re.compile(r"\{FLG:[^}]+\}")


def _load_env() -> None:
    here = Path(__file__).resolve()
    for path in (here.parents[2] / ".env", here.parents[5] / ".env"):
        if path.exists():
            load_dotenv(path)
    if not os.environ.get("CENTRALA_API_KEY"):
        print("CENTRALA_API_KEY missing", file=sys.stderr)
        sys.exit(2)


def call(answer: dict, *, api_key: str) -> dict:
    response = requests.post(
        VERIFY_URL,
        json={"apikey": api_key, "task": TASK, "answer": answer},
        timeout=30,
    )
    try:
        return response.json()
    except ValueError:
        response.raise_for_status()
        raise


def fetch_needs() -> dict[str, dict[str, int]]:
    if NEEDS_PATH.exists():
        return json.loads(NEEDS_PATH.read_text())
    print(f"[fetch] {NEEDS_URL}")
    response = requests.get(NEEDS_URL, timeout=30)
    response.raise_for_status()
    NEEDS_PATH.write_text(json.dumps(response.json(), ensure_ascii=False, indent=2))
    return response.json()


def lookup_destinations(api_key: str, city_names: list[str]) -> dict[str, int]:
    placeholders = ",".join("'" + name + "'" for name in city_names)
    query = (
        "select name, destination_id from destinations where lower(name) in "
        f"({placeholders})"
    )
    data = call({"tool": "database", "query": query}, api_key=api_key)
    if data.get("code") != 170:
        raise RuntimeError(f"destinations query failed: {data}")
    mapping = {row["name"].lower(): int(row["destination_id"]) for row in data["rows"]}
    missing = [c for c in city_names if c not in mapping]
    if missing:
        raise RuntimeError(f"destinations missing for cities: {missing}")
    return mapping


def pick_creator(api_key: str) -> tuple[int, str, str]:
    """Pick an active 'Obsługa transportów' (role=2) user as the order creator."""
    data = call(
        {
            "tool": "database",
            "query": (
                "select user_id, login, birthday from users "
                "where role=2 and is_active=1 order by user_id limit 1"
            ),
        },
        api_key=api_key,
    )
    if data.get("code") != 170 or not data.get("rows"):
        raise RuntimeError(f"could not pick creator: {data}")
    row = data["rows"][0]
    return int(row["user_id"]), row["login"], row["birthday"]


def reset(api_key: str) -> list[dict]:
    data = call({"tool": "reset"}, api_key=api_key)
    if data.get("code") != 145:
        raise RuntimeError(f"reset failed: {data}")
    return data.get("orders", [])


def delete_order(api_key: str, order_id: str) -> None:
    data = call({"tool": "orders", "action": "delete", "id": order_id}, api_key=api_key)
    if data.get("code") not in (115, 100, 110):
        # codes vary; only fail loud on obvious errors
        if "error" in str(data).lower() or data.get("code", 0) < 0:
            raise RuntimeError(f"delete failed for {order_id}: {data}")
    print(f"[delete] {order_id}: {data.get('message')}")


def generate_signature(api_key: str, login: str, birthday: str, destination: int) -> str:
    data = call(
        {
            "tool": "signatureGenerator",
            "action": "generate",
            "login": login,
            "birthday": birthday,
            "destination": destination,
        },
        api_key=api_key,
    )
    if data.get("code") != 130 or "hash" not in data:
        raise RuntimeError(f"signature failed for {login}/{destination}: {data}")
    return data["hash"]


def create_order(
    api_key: str,
    *,
    title: str,
    creator_id: int,
    destination: int,
    signature: str,
) -> str:
    data = call(
        {
            "tool": "orders",
            "action": "create",
            "title": title,
            "creatorID": creator_id,
            "destination": destination,
            "signature": signature,
        },
        api_key=api_key,
    )
    if data.get("code") != 110 or "order" not in data:
        raise RuntimeError(f"create failed: {data}")
    return data["order"]["id"]


def append_items(api_key: str, order_id: str, items: dict[str, int]) -> None:
    data = call(
        {"tool": "orders", "action": "append", "id": order_id, "items": items},
        api_key=api_key,
    )
    if data.get("code", 0) < 0:
        raise RuntimeError(f"append failed for {order_id}: {data}")


def find_flag(payload: Any) -> str | None:
    match = FLAG_RE.search(json.dumps(payload, ensure_ascii=False))
    return match.group(0) if match else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Solve foodwarehouse task.")
    parser.add_argument("--keep-seeds", action="store_true",
                        help="Do not delete the seeded orders after reset.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the plan, but do not POST anything besides reads.")
    args = parser.parse_args()

    _load_env()
    api_key = os.environ["CENTRALA_API_KEY"]

    needs = fetch_needs()
    cities = sorted(needs.keys())
    print(f"[needs] {len(cities)} cities: {cities}")

    destinations = lookup_destinations(api_key, cities)
    print("[destinations]")
    for city in cities:
        print(f"  {city:<14} -> {destinations[city]}")

    creator_id, login, birthday = pick_creator(api_key)
    print(f"[creator] user_id={creator_id} login={login} birthday={birthday}")

    if args.dry_run:
        print("[dry-run] would reset, delete seeds, create 8 orders, call done.")
        return 0

    seed_orders = reset(api_key)
    print(f"[reset] seeded with {len(seed_orders)} order(s)")
    if not args.keep_seeds:
        for seed in seed_orders:
            delete_order(api_key, seed["id"])

    for city in cities:
        destination = destinations[city]
        signature = generate_signature(api_key, login, birthday, destination)
        order_id = create_order(
            api_key,
            title=f"Dostawa do {city.capitalize()}",
            creator_id=creator_id,
            destination=destination,
            signature=signature,
        )
        append_items(api_key, order_id, needs[city])
        print(f"[order] {city} -> id={order_id} ({len(needs[city])} item types)")

    print("\n--- done ---")
    result = call({"tool": "done"}, api_key=api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    flag = find_flag(result)
    if flag:
        print(f"\nFLAG: {flag}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
