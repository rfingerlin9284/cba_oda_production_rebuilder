#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════════════════
#  mega_rebuild.sh
#  Master installer / rebuilder for CBA_ODA Production Bots.
#
#  Usage (Linux / WSL):
#    bash mega_rebuild.sh [SOURCE_DIR]
#
#  If SOURCE_DIR is supplied the project is copied there first; otherwise the
#  script assumes it is already being run from inside ~/rfing.
#
#  What this script does (in order):
#    Phase 1 — System packages (Ubuntu APT)
#    Phase 2 — Python 3 virtual environments
#    Phase 3 — OANDA forex bot dependencies
#    Phase 4 — Coinbase crypto bot dependencies
#    Phase 5 — Configuration / .env bootstrapping
#    Phase 6 — Smoke-test (import checks)
# ════════════════════════════════════════════════════════════════════════════════

set -euo pipefail

# ── Colour helpers ────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'
info()    { echo -e "${CYAN}[INFO]${NC}  $*"; }
success() { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*" >&2; }
banner()  { echo -e "\n${BOLD}${CYAN}══ $* ══${NC}\n"; }

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="${1:-$SCRIPT_DIR}"
INSTALL_DIR="$HOME/rfing"
LOG_FILE="$HOME/rfing_install.log"

echo -e "\n${BOLD}"
echo "  ╔══════════════════════════════════════════════════════════╗"
echo "  ║        CBA_ODA Production Rebuilder — mega_rebuild       ║"
echo "  ║        OANDA Forex Bot + Coinbase Crypto Bot             ║"
echo "  ╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

info "All output is also logged to: $LOG_FILE"
exec > >(tee -a "$LOG_FILE") 2>&1

# ════════════════════════════════════════════════════════════════════════════════
# PHASE 1 — System packages
# ════════════════════════════════════════════════════════════════════════════════
banner "PHASE 1 — Updating system & installing packages"

sudo apt-get update -qq
sudo apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv python3-dev \
    git curl wget build-essential \
    libssl-dev libffi-dev \
    jq htop tmux

success "System packages installed."

# ════════════════════════════════════════════════════════════════════════════════
# PHASE 2 — Copy / refresh project into ~/rfing
# ════════════════════════════════════════════════════════════════════════════════
banner "PHASE 2 — Setting up project directory at $INSTALL_DIR"

if [ "$SOURCE_DIR" != "$INSTALL_DIR" ]; then
    info "Syncing project from $SOURCE_DIR -> $INSTALL_DIR ..."
    rsync -a --exclude='.git' --exclude='venv' --exclude='__pycache__' \
        "$SOURCE_DIR/" "$INSTALL_DIR/"
else
    info "Already running inside $INSTALL_DIR — skipping copy."
fi

cd "$INSTALL_DIR"
mkdir -p logs bots/oanda/data bots/coinbase/data

# ── .env setup ────────────────────────────────────────────────────────────────
if [ ! -f ".env" ]; then
    cp .env.example .env
    warn ".env created from template. Edit ~/rfing/.env with your API keys before starting the bots."
else
    info ".env already exists — leaving it untouched."
fi

success "Project directory ready."

# ════════════════════════════════════════════════════════════════════════════════
# PHASE 3 — OANDA bot virtual environment & dependencies
# ════════════════════════════════════════════════════════════════════════════════
banner "PHASE 3 — OANDA Forex Bot environment"

cd "$INSTALL_DIR/bots/oanda"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
deactivate

success "OANDA bot environment ready."

# ════════════════════════════════════════════════════════════════════════════════
# PHASE 4 — Coinbase bot virtual environment & dependencies
# ════════════════════════════════════════════════════════════════════════════════
banner "PHASE 4 — Coinbase Crypto Bot environment"

cd "$INSTALL_DIR/bots/coinbase"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
deactivate

success "Coinbase bot environment ready."

# ════════════════════════════════════════════════════════════════════════════════
# PHASE 5 — Make all scripts executable
# ════════════════════════════════════════════════════════════════════════════════
banner "PHASE 5 — Setting script permissions"

cd "$INSTALL_DIR"
chmod +x scripts/*.sh setup/*.sh mega_rebuild.sh 2>/dev/null || true

success "Permissions set."

# ════════════════════════════════════════════════════════════════════════════════
# PHASE 6 — Smoke tests (import checks)
# ════════════════════════════════════════════════════════════════════════════════
banner "PHASE 6 — Smoke tests"

cd "$INSTALL_DIR/bots/oanda"
source venv/bin/activate
python3 -c "import oandapyV20; import pandas; import numpy; print('  OANDA imports: OK')"
deactivate

cd "$INSTALL_DIR/bots/coinbase"
source venv/bin/activate
python3 -c "import coinbase; import pandas; import numpy; print('  Coinbase imports: OK')"
deactivate

success "All import checks passed."

# ════════════════════════════════════════════════════════════════════════════════
# Done
# ════════════════════════════════════════════════════════════════════════════════
echo ""
echo -e "${GREEN}${BOLD}"
echo "  ╔══════════════════════════════════════════════════════════╗"
echo "  ║   Installation Complete!                                 ║"
echo "  ╠══════════════════════════════════════════════════════════╣"
echo "  ║                                                          ║"
echo "  ║  NEXT STEPS:                                             ║"
echo "  ║  1. Edit your API credentials:                           ║"
echo "  ║       nano ~/rfing/.env                                  ║"
echo "  ║  2. Start all bots:                                      ║"
echo "  ║       cd ~/rfing && bash scripts/start_all.sh            ║"
echo "  ║  3. Monitor logs:                                        ║"
echo "  ║       bash scripts/monitor.sh                            ║"
echo "  ║                                                          ║"
echo "  ║  See docs/ for phase-by-phase guidance.                  ║"
echo "  ╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"
