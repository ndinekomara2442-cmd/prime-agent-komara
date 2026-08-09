#!/usr/bin/env bash
# Komara Agency — Run test suite
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .venv ]; then
  source .venv/bin/activate
fi

echo "Running lint checks..."
flake8 . --max-line-length=120 --extend-ignore=E203,W503

echo "Running tests..."
pytest tests/ -v --tb=short
