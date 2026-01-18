#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$ROOT_DIR/.venv/bin/python3"

mkdir -p "$ROOT_DIR/logs/runs"
RUN_ID="$(date -u +"%Y%m%d_%H%M%S")"
LOG_FILE="$ROOT_DIR/logs/runs/run_${RUN_ID}.log"

# tee: console + file
exec > >(tee -a "$LOG_FILE") 2>&1

echo "=== FlightOps run start ==="
echo "run_id: $RUN_ID"
echo "root: $ROOT_DIR"
echo "python: $PY"
echo "utc: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo

echo "[1/5] fetch_states"
"$PY" src/flightops/fetch_states.py
echo

echo "[2/5] build_silver"
"$PY" src/flightops/build_silver.py
echo

echo "[3/5] kpi_report"
"$PY" src/flightops/kpi_report.py
echo

echo "[4/5] region_kpi_report"
"$PY" src/flightops/region_kpi_report.py
echo

echo "[5/5] upload_to_s3"
./scripts/upload_to_s3.sh
echo

echo "=== FlightOps run OK ==="
echo "log_file: $LOG_FILE"
