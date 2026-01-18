import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

EU = {
    "Austria","Belgium","Bulgaria","Croatia","Cyprus","Czech Republic","Denmark","Estonia","Finland","France",
    "Germany","Greece","Hungary","Ireland","Italy","Latvia","Lithuania","Luxembourg","Malta","Netherlands",
    "Poland","Portugal","Romania","Slovakia","Slovenia","Spain","Sweden",
    # extra Europe/EEA-ish (optional but useful for aviation)
    "Norway","Switzerland","United Kingdom","Iceland"
}
US_CA = {"United States","Canada"}
ASIA = {
    "China","Japan","South Korea","Korea, Republic of","India","Pakistan","Bangladesh","Sri Lanka","Nepal",
    "Thailand","Vietnam","Malaysia","Singapore","Indonesia","Philippines","Taiwan","Hong Kong",
    "United Arab Emirates","Saudi Arabia","Qatar","Kuwait","Oman","Israel","Turkey"
}

def latest_silver_file() -> Path:
    files = sorted(Path("data/silver").glob("silver_*.parquet"))
    if not files:
        raise FileNotFoundError("No silver files found in data/silver.")
    return files[-1]

def region_for_country(c: str) -> str:
    if not c:
        return "Other"
    if c in EU:
        return "EU"
    if c in US_CA:
        return "US_CA"
    if c in ASIA:
        return "ASIA"
    return "Other"

def main() -> None:
    p = latest_silver_file()
    df = pd.read_parquet(p)

    df["origin_country"] = df.get("origin_country").astype("string")
    df["region"] = df["origin_country"].fillna("").map(region_for_country)

    def agg(g: pd.DataFrame) -> dict:
        out = {
            "aircraft_total": int(len(g)),
            "on_ground": int(g["on_ground"].fillna(False).astype(bool).sum()) if "on_ground" in g else None,
            "dq_ok_rate": float(g["dq_ok"].mean()) if "dq_ok" in g and len(g) else None,
            "avg_velocity_ms": float(g["velocity"].dropna().mean()) if "velocity" in g and g["velocity"].notna().any() else None,
        }
        return out

    regions = {}
    for r, g in df.groupby("region"):
        regions[r] = agg(g)

    out = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_file": str(p),
        "regions": regions,
    }

    out_dir = Path("data/reports")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "region_kpi_latest.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print(f"Wrote: {out_path}")
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
