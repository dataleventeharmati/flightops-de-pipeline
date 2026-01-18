import json
from pathlib import Path

import pandas as pd

COLUMNS = [
    "icao24",
    "callsign",
    "origin_country",
    "time_position",
    "last_contact",
    "longitude",
    "latitude",
    "baro_altitude",
    "on_ground",
    "velocity",
    "true_track",
    "vertical_rate",
    "sensors",
    "geo_altitude",
    "squawk",
    "spi",
    "position_source",
]


def latest_raw_file() -> Path:
    files = sorted(Path("data/raw").glob("states_*.json"))
    if not files:
        raise FileNotFoundError("No raw files found in data/raw. Run fetch_states.py first.")
    return files[-1]


def main() -> None:
    raw_path = latest_raw_file()
    payload = json.loads(raw_path.read_text(encoding="utf-8"))
    states = payload.get("states") or []

    df = pd.DataFrame(states, columns=COLUMNS)

    df["callsign"] = df["callsign"].astype("string").str.strip()
    df["origin_country"] = df["origin_country"].astype("string")

    for col in [
        "longitude",
        "latitude",
        "baro_altitude",
        "geo_altitude",
        "velocity",
        "true_track",
        "vertical_rate",
    ]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["dq_has_position"] = df["latitude"].notna() & df["longitude"].notna()
    df["dq_velocity_ok"] = df["velocity"].isna() | ((df["velocity"] >= 0) & (df["velocity"] <= 400))
    df["dq_ok"] = df["dq_has_position"] & df["dq_velocity_ok"]

    out_dir = Path("data/silver")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / raw_path.name.replace("states_", "silver_").replace(".json", ".parquet")

    df.to_parquet(out_path, index=False)

    dq_rate = df["dq_ok"].mean() if len(df) else 0.0
    print(f"Built: {out_path}")
    print(f"Rows: {len(df)} | dq_ok: {int(df['dq_ok'].sum())} | dq_ok_rate: {dq_rate:.3f}")


if __name__ == "__main__":
    main()
