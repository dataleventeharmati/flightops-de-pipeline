from flightops.kpi_report import latest_silver_file
from pathlib import Path
import pytest

def test_latest_silver_file_requires_existing_data():
    if not list(Path("data/silver").glob("silver_*.parquet")):
        with pytest.raises(FileNotFoundError):
            latest_silver_file()
    else:
        path = latest_silver_file()
        assert path.exists()
        assert path.suffix == ".parquet"
