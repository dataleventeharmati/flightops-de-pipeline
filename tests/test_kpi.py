import pandas as pd

def test_kpi_metrics_basic():
    df = pd.DataFrame({
        "dq_ok": [True, True, False],
        "velocity": [100, 200, None],
        "on_ground": [False, True, False],
        "origin_country": ["DE", "DE", "FR"]
    })

    kpi = {
        "aircraft_total": int(len(df)),
        "dq_ok": int(df["dq_ok"].sum()),
        "dq_ok_rate": float(df["dq_ok"].mean()),
        "avg_velocity_ms": float(df["velocity"].dropna().mean()),
        "on_ground": int(df["on_ground"].fillna(False).astype(bool).sum()),
    }

    assert kpi["aircraft_total"] == 3
    assert kpi["dq_ok"] == 2
    assert kpi["dq_ok_rate"] > 0.6
    assert kpi["avg_velocity_ms"] == 150
    assert kpi["on_ground"] == 1
