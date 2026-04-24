#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════════════════
#  setup/03_oanda_env.sh
#  Create the Python virtual environment for the OANDA bot and install deps.
# ════════════════════════════════════════════════════════════════════════════════
set -euo pipefail

RFING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BOT_DIR="$RFING_DIR/bots/oanda"

echo "[setup/03] Setting up OANDA bot Python environment..."

cd "$BOT_DIR"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt
deactivate

echo "[setup/03] OANDA bot environment ready at $BOT_DIR/venv"
