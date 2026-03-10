#!/usr/bin/env bash
set -euo pipefail

# go to project root (works even if called from elsewhere)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# activate venv
source .venv/bin/activate

# run pipeline
./scripts/run_all.sh >> logs/scheduled_runs.log 2>&1

# add separator
echo "----" >> logs/scheduled_runs.log
