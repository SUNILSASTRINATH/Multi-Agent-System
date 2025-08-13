#!/usr/bin/env bash
set -euo pipefail

# Prefer Python 3.13 if available, else fallback
if command -v python3.13 >/dev/null 2>&1; then
  PY=python3.13
elif command -v python3 >/dev/null 2>&1; then
  PY=python3
else
  PY=python
fi

cd "$(dirname "$0")/.."
"$PY" -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
