#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi
export PYTHONPATH="src:${PYTHONPATH:-}"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --app-dir src
