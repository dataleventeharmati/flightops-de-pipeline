#!/usr/bin/env bash
set -euo pipefail

BUCKET="s3://flightops-de-pipeline-levente-2026"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Project root: $ROOT_DIR"

# Latest silver parquet
SILVER="$(ls -t "$ROOT_DIR"/data/silver/silver_*.parquet | head -n 1)"
echo "Uploading silver: $SILVER"
aws s3 cp "$SILVER" "$BUCKET/silver/$(basename "$SILVER")"

# KPI reports
for f in \
  "$ROOT_DIR/data/reports/kpi_latest.json" \
  "$ROOT_DIR/data/reports/region_kpi_latest.json"
do
  if [[ -f "$f" ]]; then
    echo "Uploading report: $f"
    aws s3 cp "$f" "$BUCKET/reports/$(basename "$f")"
  fi
done

# KPI history (append-only)
if [[ -d "$ROOT_DIR/data/reports/history" ]]; then
  echo "Uploading KPI history"
  aws s3 sync "$ROOT_DIR/data/reports/history" "$BUCKET/reports/history"
fi

echo "S3 upload complete."
