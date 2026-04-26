#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════════════════
#  scripts/start_all.sh — Start both OANDA and Coinbase bots
#  Run from: ~/rfing
# ════════════════════════════════════════════════════════════════════════════════
set -euo pipefail

RFING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$RFING_DIR/logs"
mkdir -p "$LOG_DIR"

# ── helpers ───────────────────────────────────────────────────────────────────
start_bot() {
    local name="$1"
    local bot_dir="$2"
    local pid_file="$LOG_DIR/${name}.pid"

    if [ -f "$pid_file" ] && kill -0 "$(cat "$pid_file")" 2>/dev/null; then
        echo "[SKIP] $name is already running (PID $(cat "$pid_file"))."
        return
    fi

    echo "[START] $name ..."
    cd "$bot_dir"
    source venv/bin/activate
    nohup python main.py >> "$LOG_DIR/${name}.log" 2>&1 &
    echo $! > "$pid_file"
    deactivate
    echo "  → PID $(cat "$pid_file") | log: $LOG_DIR/${name}.log"
}

echo ""
echo "══ Starting all bots ══"
start_bot "oanda"    "$RFING_DIR/bots/oanda"
start_bot "coinbase" "$RFING_DIR/bots/coinbase"
echo ""
echo "All bots started.  Use 'bash scripts/monitor.sh' to tail logs."
echo ""
