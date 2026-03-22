from flightops.kpi_report import latest_silver_file

def test_latest_silver_file_returns_path():
    path = latest_silver_file()
    assert path.exists()
    assert path.suffix == ".parquet"
