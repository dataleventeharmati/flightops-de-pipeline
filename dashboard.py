import json
from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st

KPI_LATEST = Path("data/reports/kpi_latest.json")
KPI_HISTORY_DIR = Path("data/reports/history")
REGION_KPI = Path("data/reports/region_kpi_latest.json")
SILVER_DIR = Path("data/silver")


def latest_silver() -> Path | None:
    files = sorted(SILVER_DIR.glob("silver_*.parquet"))
    return files[-1] if files else None


def load_history() -> pd.DataFrame:
    rows = []
    files = sorted(KPI_HISTORY_DIR.glob("kpi_*.json"))
    for f in files:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            ts = d.get("generated_at_utc")
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00")) if ts else None
            rows.append(
                {
                    "generated_at_utc": dt,
                    "aircraft_total": d.get("aircraft_total"),
                    "dq_ok_rate": d.get("dq_ok_rate"),
                    "on_ground": d.get("on_ground"),
                    "avg_velocity_ms": d.get("avg_velocity_ms"),
                    "max_velocity_ms": d.get("max_velocity_ms"),
                    "source_file": d.get("source_file"),
                }
            )
        except Exception:
            continue
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("generated_at_utc")
    return df


st.set_page_config(page_title="FlightOps-DE Dashboard", layout="wide")
st.title("✈️ FlightOps-DE Dashboard")
st.caption("Live aviation data (OpenSky) → raw → silver → KPI")

colA, colB, colC = st.columns([1, 1, 1])
with colA:
    if st.button("Run pipeline (fetch → silver → KPI)"):
        import subprocess
        res = subprocess.run(["./scripts/run_all.sh"], capture_output=True, text=True)
        st.code(res.stdout or "", language="text")
        if res.stderr:
            st.error(res.stderr)

with colB:
    if st.button("Build region KPI"):
        import subprocess
        res = subprocess.run(["python3", "src/flightops/region_kpi_report.py"], capture_output=True, text=True)
        st.code(res.stdout or "", language="text")
        if res.stderr:
            st.error(res.stderr)

with colC:
    st.write("")

st.divider()

st.subheader("📌 Latest KPI")
if KPI_LATEST.exists():
    kpi = json.loads(KPI_LATEST.read_text(encoding="utf-8"))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Aircraft total", kpi.get("aircraft_total"))
    c2.metric("On ground", kpi.get("on_ground"))
    c3.metric("Avg velocity (m/s)", None if kpi.get("avg_velocity_ms") is None else round(kpi["avg_velocity_ms"], 2))
    c4.metric("Max velocity (m/s)", None if kpi.get("max_velocity_ms") is None else round(kpi["max_velocity_ms"], 2))
    st.json(kpi, expanded=False)
else:
    st.warning("No KPI file found. Run the pipeline first.")

st.divider()

st.subheader("🌍 Regional breakdown (EU / US_CA / ASIA / Other)")
if REGION_KPI.exists():
    rk = json.loads(REGION_KPI.read_text(encoding="utf-8"))
    regions = rk.get("regions", {})

    order = ["EU", "US_CA", "ASIA", "Other"]
    cols = st.columns(4)
    for i, name in enumerate(order):
        d = regions.get(name, {})
        cols[i].metric(
            f"{name} aircraft",
            d.get("aircraft_total"),
            help=f"on_ground={d.get('on_ground')} | dq_ok_rate={d.get('dq_ok_rate')}",
        )

    # Table view
    table = []
    for name, d in regions.items():
        table.append(
            {
                "region": name,
                "aircraft_total": d.get("aircraft_total"),
                "on_ground": d.get("on_ground"),
                "dq_ok_rate": d.get("dq_ok_rate"),
                "avg_velocity_ms": d.get("avg_velocity_ms"),
            }
        )
    st.dataframe(pd.DataFrame(table).sort_values("aircraft_total", ascending=False), use_container_width=True)
else:
    st.info("No region KPI file yet. Click 'Build region KPI' or run it in terminal.")

st.divider()

st.subheader("🏎️ Velocity distribution (latest silver)")
p_silver = latest_silver()
if p_silver is None:
    st.info("No silver file yet.")
else:
    dfv = pd.read_parquet(p_silver)
    if "velocity" in dfv:
        v = dfv["velocity"].dropna()
        v = v[(v >= 0) & (v <= 400)]  # keep sane range
        if len(v) == 0:
            st.info("No velocity values available.")
        else:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("count", int(len(v)))
            c2.metric("p50 (m/s)", float(v.quantile(0.50)))
            c3.metric("p90 (m/s)", float(v.quantile(0.90)))
            c4.metric("p99 (m/s)", float(v.quantile(0.99)))

            st.bar_chart(v.value_counts(bins=40).sort_index())
            st.caption(f"Source: {p_silver} | range used: 0..400 m/s")
    else:
        st.info("velocity column not found.")


st.divider()

st.subheader("📈 KPI trend (history)")
hist = load_history()
if hist.empty:
    st.info("No KPI history found yet. Run the pipeline a few times to build history.")
else:
    left, right = st.columns(2)
    with left:
        st.line_chart(hist.set_index("generated_at_utc")[["aircraft_total", "on_ground"]])
    with right:
        st.line_chart(hist.set_index("generated_at_utc")[["dq_ok_rate"]])

    st.dataframe(hist.tail(20), use_container_width=True)

st.divider()

st.subheader("🗺️ Aircraft positions (global view)")
p = latest_silver()
if p is None:
    st.warning("No silver parquet found. Run the pipeline first.")
else:
    df = pd.read_parquet(p)

    if "latitude" in df and "longitude" in df:
        df_pos = df[df["latitude"].notna() & df["longitude"].notna()].copy()

        max_points = st.slider("Max points to display", 500, 6000, 3000, 500)
        if len(df_pos) > max_points:
            df_pos = df_pos.sample(n=max_points, random_state=42)

        st.map(df_pos.rename(columns={"latitude": "lat", "longitude": "lon"})[["lat", "lon"]])

        st.caption(
            f"Source: {p} | points shown: {len(df_pos)} | "
            f"lat[{df['latitude'].min():.2f}, {df['latitude'].max():.2f}] "
            f"lon[{df['longitude'].min():.2f}, {df['longitude'].max():.2f}]"
        )

        st.dataframe(
            df_pos[["icao24", "callsign", "origin_country", "latitude", "longitude", "velocity", "on_ground", "dq_ok"]].head(50),
            use_container_width=True,
        )
    else:
        st.error("latitude/longitude columns not found in silver.")
