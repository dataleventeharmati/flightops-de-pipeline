#!/usr/bin/env bash
set -euo pipefail

python3 src/flightops/fetch_states.py
python3 src/flightops/build_silver.py
python3 src/flightops/kpi_report.py
