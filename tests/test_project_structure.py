from __future__ import annotations

from pathlib import Path


def test_key_project_files_exist():
    expected = [
        Path("README.md"),
        Path("pyproject.toml"),
        Path(".github/workflows/ci.yml"),
        Path("dashboard.py"),
        Path("src/flightops/__init__.py"),
        Path("src/flightops/fetch_states.py"),
        Path("src/flightops/build_silver.py"),
        Path("src/flightops/kpi_report.py"),
        Path("src/flightops/region_kpi_report.py"),
    ]
    for path in expected:
        assert path.exists(), f"Missing expected file: {path}"
