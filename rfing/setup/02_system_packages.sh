#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════════════════
#  setup/02_system_packages.sh
#  Install all Ubuntu system-level packages required by both bots.
#  Called automatically by mega_rebuild.sh — can also be run standalone.
# ════════════════════════════════════════════════════════════════════════════════
set -euo pipefail

echo "[setup/02] Updating APT and installing system packages..."
sudo apt-get update -qq
sudo apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    git \
    curl \
    wget \
    build-essential \
    libssl-dev \
    libffi-dev \
    jq \
    htop \
    tmux

echo "[setup/02] Done."
