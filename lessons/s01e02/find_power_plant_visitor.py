import json
import math
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from aidevs4.centrala import submit_answer

LOCATIONS_PATH = Path(__file__).parent / "findhim_locations.json"
HUB = "https://hub.ag3nts.org"
NOMINATIM = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "aidevs4-s01e02/1.0 (educational; contact: kowalskirafal32@gmail.com)"
NEAR_KM = 25.0

# Suspects from S01E01 (males born in Grudziądz, age 20-40, tagged "transport").
SUSPECTS = [
    {"name": "Cezary",   "surname": "Żurek",     "birthYear": 1987},
    {"name": "Jacek",    "surname": "Nowak",     "birthYear": 1991},
    {"name": "Oskar",    "surname": "Sieradzki", "birthYear": 1993},
    {"name": "Wojciech", "surname": "Bielik",    "birthYear": 1986},
    {"name": "Wacław",   "surname": "Jasiński",  "birthYear": 1986},
]


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def geocode(city: str) -> tuple[float, float]:
    resp = requests.get(
        NOMINATIM,
        params={"q": f"{city}, Poland", "format": "json", "limit": 1},
        headers={"User-Agent": USER_AGENT},
        timeout=30,
    )
    resp.raise_for_status()
    hit = resp.json()[0]
    return float(hit["lat"]), float(hit["lon"])


def fetch_locations(api_key: str, person: dict) -> list[dict]:
    resp = requests.post(
        f"{HUB}/api/location",
        json={"apikey": api_key, "name": person["name"], "surname": person["surname"]},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def fetch_access_level(api_key: str, person: dict) -> dict:
    resp = requests.post(
        f"{HUB}/api/accesslevel",
        json={
            "apikey": api_key,
            "name": person["name"],
            "surname": person["surname"],
            "birthYear": person["birthYear"],
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def extract_coords(payload) -> list[tuple[float, float]]:
    """Tolerate a few possible shapes from /api/location."""
    if isinstance(payload, dict):
        for key in ("locations", "coords", "data", "answer", "results"):
            if key in payload and isinstance(payload[key], list):
                payload = payload[key]
                break
    if not isinstance(payload, list):
        return []
    out = []
    for item in payload:
        if isinstance(item, dict):
            lat = item.get("lat") or item.get("latitude")
            lon = item.get("lon") or item.get("lng") or item.get("longitude")
            if lat is not None and lon is not None:
                out.append((float(lat), float(lon)))
        elif isinstance(item, (list, tuple)) and len(item) >= 2:
            out.append((float(item[0]), float(item[1])))
    return out


def main() -> None:
    load_dotenv()
    api_key = os.environ["CENTRALA_API_KEY"]

    plants_raw = json.loads(LOCATIONS_PATH.read_text(encoding="utf-8"))["power_plants"]
    plants = []
    for city, info in plants_raw.items():
        lat, lon = geocode(city)
        plants.append({"city": city, "code": info["code"], "lat": lat, "lon": lon})
        print(f"  plant {city:22s} {info['code']}  ({lat:.4f}, {lon:.4f})")

    candidates = []  # (distance_km, suspect, plant)
    for s in SUSPECTS:
        try:
            payload = fetch_locations(api_key, s)
        except requests.HTTPError as e:
            print(f"  {s['name']} {s['surname']}: HTTP {e.response.status_code} — skipped")
            continue
        coords = extract_coords(payload)
        print(f"\n{s['name']} {s['surname']}: {len(coords)} location(s)")
        if not coords:
            print(f"  raw: {json.dumps(payload, ensure_ascii=False)[:200]}")
            continue
        suspect_best = None
        for lat, lon in coords:
            for plant in plants:
                d = haversine_km(lat, lon, plant["lat"], plant["lon"])
                if suspect_best is None or d < suspect_best[0]:
                    suspect_best = (d, plant, lat, lon)
        d, plant, lat, lon = suspect_best
        print(f"  closest: {plant['city']:22s} {d:7.2f} km  (point {lat:.4f},{lon:.4f})")
        if d <= NEAR_KM:
            candidates.append((d, s, plant))

    candidates.sort(key=lambda x: x[0])

    if not candidates:
        raise SystemExit(f"No suspect within {NEAR_KM} km of a plant.")

    print(f"\n{len(candidates)} candidate(s) within {NEAR_KM} km — trying closest first:")
    for distance, suspect, plant in candidates:
        access = fetch_access_level(api_key, suspect)
        access_level = access.get("accessLevel") or access.get("access_level")
        answer = {
            "name": suspect["name"],
            "surname": suspect["surname"],
            "accessLevel": access_level,
            "powerPlant": plant["code"],
        }
        print(f"\n→ {suspect['name']} {suspect['surname']} @ {plant['city']}"
              f" ({plant['code']}, {distance:.2f} km, accessLevel={access_level})")
        try:
            result = submit_answer("findhim", answer)
        except requests.HTTPError as e:
            print(f"  rejected: {e}")
            continue
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    raise SystemExit("All candidates rejected by /verify.")


if __name__ == "__main__":
    main()
