#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════════════════
#  scripts/monitor.sh — Tail live logs for both bots (split view with tmux)
#  Falls back to sequential tail if tmux is not available.
# ════════════════════════════════════════════════════════════════════════════════
RFING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$RFING_DIR/logs"

ODA_LOG="$LOG_DIR/oanda.log"
CBA_LOG="$LOG_DIR/coinbase.log"

# ── ensure log files exist ────────────────────────────────────────────────────
touch "$ODA_LOG" "$CBA_LOG"

echo ""
echo "══ Bot Log Monitor ══"
echo "  OANDA log    : $ODA_LOG"
echo "  Coinbase log : $CBA_LOG"
echo ""

if command -v tmux &>/dev/null; then
    SESSION="rfing_monitor"
    tmux kill-session -t "$SESSION" 2>/dev/null || true
    tmux new-session -d -s "$SESSION"
    tmux split-window -h -t "$SESSION"
    tmux send-keys -t "$SESSION:0.0" "tail -F '$ODA_LOG'" Enter
    tmux send-keys -t "$SESSION:0.1" "tail -F '$CBA_LOG'" Enter
    tmux attach-session -t "$SESSION"
else
    echo "tmux not found — tailing OANDA log only. Install tmux for split view."
    echo "Press Ctrl+C to stop."
    tail -F "$ODA_LOG"
fi
