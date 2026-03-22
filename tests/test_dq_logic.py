import pandas as pd

def test_dq_flags_logic():
    df = pd.DataFrame({
        "latitude": [10.0, None],
        "longitude": [20.0, 30.0],
        "velocity": [100, 500]  # 500 invalid
    })

    df["dq_has_position"] = df["latitude"].notna() & df["longitude"].notna()
    df["dq_velocity_ok"] = df["velocity"].isna() | ((df["velocity"] >= 0) & (df["velocity"] <= 400))
    df["dq_ok"] = df["dq_has_position"] & df["dq_velocity_ok"]

    assert df["dq_has_position"].tolist() == [True, False]
    assert df["dq_velocity_ok"].tolist() == [True, False]
    assert df["dq_ok"].tolist() == [True, False]
