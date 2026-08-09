#!/usr/bin/env bash
# Komara Agency — Prime Agent installer
set -euo pipefail

echo "Installing Komara Agency Prime Agent..."

PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" &> /dev/null; then
  echo "Error: python3 not found. Install Python 3.12+ first." >&2
  exit 1
fi

"$PYTHON_BIN" -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example — fill in your tokens before running."
fi

echo "Installation complete."
echo "Run: source .venv/bin/activate && ./prime-agent.sh"
