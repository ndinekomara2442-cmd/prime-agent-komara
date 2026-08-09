#!/usr/bin/env bash
# Komara Agency — Prime Agent launcher
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .venv ]; then
  source .venv/bin/activate
fi

export PYTHONPATH="${PYTHONPATH:-.}"

exec python3 main.py "$@"
