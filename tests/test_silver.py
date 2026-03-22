import pandas as pd
from flightops.build_silver import COLUMNS

def test_silver_schema_columns():
    # fake raw states (1 row)
    row = [
        "abc123", "TEST123", "Germany", 1, 1,
        10.0, 20.0, 1000, False, 200, 180, 0,
        None, 1000, None, False, 0
    ]

    df = pd.DataFrame([row], columns=COLUMNS)

    # basic expectations
    assert "latitude" in df.columns
    assert "longitude" in df.columns
    assert len(df) == 1
