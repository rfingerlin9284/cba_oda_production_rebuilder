#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════════════════
#  scripts/stop_all.sh — Stop all running bots gracefully
#  Run from: ~/rfing
# ════════════════════════════════════════════════════════════════════════════════
set -euo pipefail

RFING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$RFING_DIR/logs"
MAX_SHUTDOWN_WAIT_SEC=10

stop_bot() {
    local name="$1"
    local pid_file="$LOG_DIR/${name}.pid"

    if [ ! -f "$pid_file" ]; then
        echo "[SKIP] $name — no PID file found."
        return
    fi

    local pid
    pid="$(cat "$pid_file")"

    if kill -0 "$pid" 2>/dev/null; then
        echo "[STOP] $name (PID $pid) ..."
        kill -TERM "$pid"
        # Wait up to MAX_SHUTDOWN_WAIT_SEC seconds for clean shutdown
        for _ in $(seq 1 "$MAX_SHUTDOWN_WAIT_SEC"); do
            kill -0 "$pid" 2>/dev/null || break
            sleep 1
        done
        # Force kill if still running
        if kill -0 "$pid" 2>/dev/null; then
            kill -KILL "$pid"
            echo "  → $name force-killed."
        else
            echo "  → $name stopped cleanly."
        fi
    else
        echo "[SKIP] $name — PID $pid is not running."
    fi

    rm -f "$pid_file"
}

echo ""
echo "══ Stopping all bots ══"
stop_bot "oanda"
stop_bot "coinbase"
echo ""
echo "Done."
