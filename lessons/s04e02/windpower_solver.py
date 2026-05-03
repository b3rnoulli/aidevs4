"""S04E02 `windpower` solver — schedules a wind turbine within the 40s window.

Strategy (everything after `start` runs in parallel):
1. POST start.
2. Concurrently queue weather + powerplantcheck.
3. Drain getResult (parallel pollers) until both reports arrive.
4. Build configs:
   - Storm protection (pitch=90, idle) at the START of each contiguous wind>14 m/s window.
   - Production (pitch=0, production) at the first hour where the LOWER-bound wind yield
     covers the deficit reported by powerplantcheck.
5. Compute unlockCodes locally via MD5 of `startDate|startHour|windMs|pitchAngle`
   (the format we cracked offline matched the API's `unlockCodeGenerator` output).
6. POST config (batch).
7. Queue turbinecheck → drain getResult.
8. POST done; print the flag.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import requests
from dotenv import load_dotenv

URL = "https://hub.ag3nts.org/verify"
TASK = "windpower"

# Yield % at pitch 0 from the documentation. The doc gives a range (e.g. 30-40 at 6 m/s);
# we keep both bounds. Use UB to decide whether an hour CAN produce at least the deficit.
WIND_YIELD_LB = [(4, 10), (6, 30), (8, 60), (10, 90), (12, 100), (14, 100)]
WIND_YIELD_UB = [(4, 15), (6, 40), (8, 70), (10, 100), (12, 100), (14, 100)]
RATED_KW = 14
CUTOFF_WIND = 14  # > this -> storm


# ---------------------------------------------------------------------------
# API plumbing
# ---------------------------------------------------------------------------

def make_call(api_key: str):
    sess = requests.Session()

    def call(answer: dict, *, timeout: float = 15) -> dict:
        payload = {"apikey": api_key, "task": TASK, "answer": answer}
        try:
            r = sess.post(URL, json=payload, timeout=timeout)
        except requests.RequestException as exc:
            return {"_error": f"network: {exc}"}
        try:
            return r.json()
        except ValueError:
            return {"_status": r.status_code, "_text": r.text[:500]}

    return call


def unlock_code(date: str, hour: str, wind_ms: float, pitch_deg: float) -> str:
    s = f"{date}|{hour}|{float(wind_ms):.1f}|{float(pitch_deg):.1f}"
    return hashlib.md5(s.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Weather + plant parsing
# ---------------------------------------------------------------------------

def _yield_lerp(wind_ms: float, table: list[tuple[int, int]]) -> float:
    """Linear interpolation between bucket points; clamp outside."""
    if wind_ms < table[0][0] or wind_ms > 14:
        return 0.0
    for (w1, y1), (w2, y2) in zip(table, table[1:]):
        if w1 <= wind_ms <= w2:
            if w2 == w1:
                return float(y1)
            return y1 + (wind_ms - w1) / (w2 - w1) * (y2 - y1)
    return float(table[-1][1])


def power_kw(wind_ms: float, pitch_deg: float = 0, *, mode: str = "mid") -> float:
    """Estimated kW at given wind/pitch. mode: 'lb' / 'ub' / 'mid'."""
    if pitch_deg == 90:
        return 0.0
    pitch_yield = {0: 100, 45: 65, 90: 0}[pitch_deg]
    lb = _yield_lerp(wind_ms, WIND_YIELD_LB)
    ub = _yield_lerp(wind_ms, WIND_YIELD_UB)
    y = lb if mode == "lb" else ub if mode == "ub" else (lb + ub) / 2
    return RATED_KW * y / 100 * pitch_yield / 100


def split_ts(ts: str) -> tuple[str, str]:
    """'2026-03-30 14:00:00' or '2026-03-30T14:00:00' -> ('2026-03-30', '14:00:00')."""
    ts = ts.strip().replace("T", " ")
    if " " in ts:
        d, h = ts.split(" ", 1)
    else:
        d, h = ts[:10], ts[10:]
    h = h[:8] if len(h) >= 8 else h
    return d, h


def extract_hourly(weather_resp: dict) -> list[dict]:
    """Coerce the weather response into a list of {timestamp, windMs} sorted by time."""
    candidates = ["forecast", "weather", "data", "items", "hours", "hourly"]
    rows = None
    for k in candidates:
        v = weather_resp.get(k)
        if isinstance(v, list) and v:
            rows = v
            break
    if rows is None:
        # maybe top-level list?
        for v in weather_resp.values():
            if isinstance(v, list) and v and isinstance(v[0], dict):
                rows = v
                break
    if rows is None:
        raise ValueError(f"Could not find hourly list in weather response: {list(weather_resp)}")

    out: list[dict] = []
    for row in rows:
        ts = (row.get("timestamp") or row.get("time") or row.get("hour")
              or row.get("datetime") or row.get("date"))
        wind = (row.get("windMs") if "windMs" in row else
                row.get("wind") if "wind" in row else
                row.get("windSpeed") if "windSpeed" in row else
                row.get("speed"))
        if ts is None or wind is None:
            continue
        try:
            wind_f = float(wind)
        except (TypeError, ValueError):
            continue
        out.append({"timestamp": str(ts), "windMs": wind_f})
    out.sort(key=lambda r: r["timestamp"])
    return out


def _coerce_kw_range(value: Any) -> tuple[float, float] | None:
    """Parse '5', 5, '4-5', '4.5' etc. into (lo, hi) tuple."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value), float(value)
    s = str(value).strip().replace("kW", "").replace("kw", "").strip()
    if "-" in s:
        parts = [p for p in s.split("-") if p]
        try:
            nums = [float(p) for p in parts]
            return min(nums), max(nums)
        except ValueError:
            return None
    try:
        n = float(s)
        return n, n
    except ValueError:
        return None


def extract_deficit_range(plant_resp: dict) -> tuple[float, float]:
    keys = ("missingPowerKw", "deficitKw", "powerNeededKw", "missingKw",
            "deficit", "neededKw", "powerDeficit", "powerDeficitKw", "missingPower")
    for k in keys:
        if k in plant_resp:
            v = _coerce_kw_range(plant_resp[k])
            if v is not None:
                return v
    for k, v in plant_resp.items():
        if "power" in k.lower() or "kw" in k.lower() or "deficit" in k.lower() or "missing" in k.lower():
            parsed = _coerce_kw_range(v)
            if parsed is not None:
                return parsed
    raise ValueError(f"Could not extract deficit from plant response: {plant_resp}")


def find_storm_starts(forecast: list[dict]) -> list[dict]:
    """Return one entry per contiguous wind > CUTOFF_WIND group, at its first hour."""
    starts: list[dict] = []
    in_storm = False
    for row in forecast:
        if row["windMs"] > CUTOFF_WIND:
            if not in_storm:
                starts.append(row)
                in_storm = True
        else:
            in_storm = False
    return starts


def find_production_hour(forecast: list[dict], deficit_lo: float, deficit_hi: float) -> dict:
    """First hour where MIDPOINT yield at pitch=0 covers the MIDPOINT deficit."""
    target = (deficit_lo + deficit_hi) / 2
    for row in forecast:
        if row["windMs"] > CUTOFF_WIND:
            continue
        if power_kw(row["windMs"], 0, mode="mid") >= target:
            return row
    # Fall back: pick the hour with the highest UB power at pitch=0.
    best = max((r for r in forecast if r["windMs"] <= CUTOFF_WIND),
               key=lambda r: power_kw(r["windMs"], 0, mode="ub"), default=None)
    if best is None:
        raise RuntimeError("No non-storm hour in forecast")
    return best


# ---------------------------------------------------------------------------
# Polling
# ---------------------------------------------------------------------------

def drain_until(call, want: set[str], *, timeout: float, workers: int = 3,
                poll_pause: float = 0.25) -> dict[str, dict]:
    got: dict[str, dict] = {}
    lock = threading.Lock()
    stop = threading.Event()
    deadline = time.monotonic() + timeout

    def worker():
        while not stop.is_set() and time.monotonic() < deadline:
            r = call({"action": "getResult"})
            if r.get("code") == 12 and r.get("sourceFunction"):
                with lock:
                    if r["sourceFunction"] in want and r["sourceFunction"] not in got:
                        got[r["sourceFunction"]] = r
                        if want.issubset(got.keys()):
                            stop.set()
                            return
                    else:
                        # Not interesting (or duplicate) — keep going.
                        pass
            else:
                time.sleep(poll_pause)

    threads = [threading.Thread(target=worker, daemon=True) for _ in range(workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=timeout + 1)
    return got


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(api_key: str, *, dump_path: str | None = None) -> int:
    call = make_call(api_key)
    t0 = time.monotonic()

    def log(msg: str) -> None:
        print(f"[{time.monotonic() - t0:5.2f}s] {msg}")

    # 1. start
    r = call({"action": "start"})
    log(f"start -> {json.dumps(r, ensure_ascii=False)}")

    # 2. concurrently queue weather + powerplantcheck
    with ThreadPoolExecutor(max_workers=4) as ex:
        f1 = ex.submit(call, {"action": "get", "param": "weather"})
        f2 = ex.submit(call, {"action": "get", "param": "powerplantcheck"})
        log(f"queued weather -> {json.dumps(f1.result(), ensure_ascii=False)}")
        log(f"queued plant   -> {json.dumps(f2.result(), ensure_ascii=False)}")

    # 3. drain
    log("draining for {weather, powerplantcheck} ...")
    got = drain_until(call, {"weather", "powerplantcheck"}, timeout=30)
    log(f"got: {sorted(got.keys())}")
    if dump_path:
        with open(dump_path, "w") as f:
            json.dump(got, f, ensure_ascii=False, indent=2)
    if "weather" not in got or "powerplantcheck" not in got:
        log(f"missing reports; raw got = {json.dumps(got, ensure_ascii=False, indent=2)}")
        return 2

    # 4. parse
    log(f"raw weather keys: {list(got['weather'])}")
    forecast = extract_hourly(got["weather"])
    log(f"forecast hours: {len(forecast)}; first={forecast[0] if forecast else None}; "
        f"last={forecast[-1] if forecast else None}")
    log(f"raw plant: {json.dumps(got['powerplantcheck'], ensure_ascii=False)}")
    deficit_lo, deficit_hi = extract_deficit_range(got["powerplantcheck"])
    log(f"deficit range = {deficit_lo} .. {deficit_hi} kW")

    # 5. plan configs
    storm_starts = find_storm_starts(forecast)
    log(f"storm-start rows: {[(r['timestamp'], r['windMs']) for r in storm_starts]}")
    prod_row = find_production_hour(forecast, deficit_lo, deficit_hi)
    log(f"production hour: ts={prod_row['timestamp']}, wind={prod_row['windMs']} m/s, "
        f"power(lb/mid/ub) = {power_kw(prod_row['windMs'],0,mode='lb'):.2f} / "
        f"{power_kw(prod_row['windMs'],0,mode='mid'):.2f} / "
        f"{power_kw(prod_row['windMs'],0,mode='ub'):.2f} kW")

    configs: dict[str, dict] = {}
    for row in storm_starts:
        d, h = split_ts(row["timestamp"])
        configs[f"{d} {h}"] = {
            "pitchAngle": 90,
            "turbineMode": "idle",
            "unlockCode": unlock_code(d, h, row["windMs"], 90),
        }
    pd, ph = split_ts(prod_row["timestamp"])
    configs[f"{pd} {ph}"] = {
        "pitchAngle": 0,
        "turbineMode": "production",
        "unlockCode": unlock_code(pd, ph, prod_row["windMs"], 0),
    }
    log(f"config plan ({len(configs)} points):\n" +
        json.dumps(configs, ensure_ascii=False, indent=2))

    # 6. send config (batch)
    r = call({"action": "config", "configs": configs})
    log(f"config -> {json.dumps(r, ensure_ascii=False)}")

    # 7. queue turbinecheck
    r = call({"action": "get", "param": "turbinecheck"})
    log(f"queued turbinecheck -> {json.dumps(r, ensure_ascii=False)}")

    # 8. drain
    got2 = drain_until(call, {"turbinecheck"}, timeout=20)
    log(f"turbinecheck result -> {json.dumps(got2.get('turbinecheck'), ensure_ascii=False)}")

    # 9. done
    final = call({"action": "done"})
    log(f"done -> {json.dumps(final, ensure_ascii=False)}")
    return 0


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--dump", help="dump raw weather/plant responses to this path")
    args = parser.parse_args()
    return run(os.environ["CENTRALA_API_KEY"], dump_path=args.dump)


if __name__ == "__main__":
    sys.exit(main())
