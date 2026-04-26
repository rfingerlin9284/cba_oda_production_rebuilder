#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════════════════
#  setup/04_coinbase_env.sh
#  Create the Python virtual environment for the Coinbase bot and install deps.
# ════════════════════════════════════════════════════════════════════════════════
set -euo pipefail

RFING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BOT_DIR="$RFING_DIR/bots/coinbase"

echo "[setup/04] Setting up Coinbase bot Python environment..."

cd "$BOT_DIR"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt
deactivate

echo "[setup/04] Coinbase bot environment ready at $BOT_DIR/venv"
