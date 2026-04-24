#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════════════════
#  scripts/status.sh — Show status of all bots
# ════════════════════════════════════════════════════════════════════════════════
RFING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$RFING_DIR/logs"

check_bot() {
    local name="$1"
    local pid_file="$LOG_DIR/${name}.pid"
    if [ -f "$pid_file" ] && kill -0 "$(cat "$pid_file")" 2>/dev/null; then
        echo "  [RUNNING] $name (PID $(cat "$pid_file"))"
    else
        echo "  [STOPPED] $name"
    fi
}

echo ""
echo "══ Bot Status ══"
check_bot "oanda"
check_bot "coinbase"
echo ""
