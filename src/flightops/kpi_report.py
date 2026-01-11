import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


def latest_silver_file() -> Path:
    files = sorted(Path("data/silver").glob("silver_*.parquet"))
    if not files:
        raise FileNotFoundError("No silver files found in data/silver. Run build_silver.py first.")
    return files[-1]


def main() -> None:
    p = latest_silver_file()
    df = pd.read_parquet(p)

    kpi = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_file": str(p),
        "aircraft_total": int(len(df)),
        "aircraft_with_position": int(df["dq_has_position"].sum()) if "dq_has_position" in df else None,
        "dq_ok": int(df["dq_ok"].sum()) if "dq_ok" in df else None,
        "dq_ok_rate": float(df["dq_ok"].mean()) if "dq_ok" in df and len(df) else None,
        "on_ground": int(df["on_ground"].fillna(False).astype(bool).sum()) if "on_ground" in df else None,
        "avg_velocity_ms": float(df["velocity"].dropna().mean()) if "velocity" in df and df["velocity"].notna().any() else None,
        "max_velocity_ms": float(df["velocity"].dropna().max()) if "velocity" in df and df["velocity"].notna().any() else None,
        "top_origin_countries": (
            df["origin_country"].dropna().value_counts().head(5).to_dict()
            if "origin_country" in df else {}
        ),
    }

    out_dir = Path("data/reports")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "kpi_latest.json"
    out_path.write_text(json.dumps(kpi, indent=2), encoding="utf-8")

    print(f"Wrote: {out_path}")
    print(json.dumps(kpi, indent=2))


if __name__ == "__main__":
    main()
