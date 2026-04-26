#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════════════════
#  setup/01_wsl_ubuntu.sh
#  Run once on a fresh Windows machine to enable WSL and install Ubuntu.
#  Must be run from an ELEVATED PowerShell — this script is a reference;
#  paste the commands manually in PowerShell if preferred.
# ════════════════════════════════════════════════════════════════════════════════
echo "This script is a reference for Windows WSL setup."
echo "Run the following commands in PowerShell (as Administrator):"
echo ""
echo "  # Enable WSL and install Ubuntu (requires reboot)"
echo "  wsl --install"
echo ""
echo "  # After reboot, set WSL 2 as default"
echo "  wsl --set-default-version 2"
echo ""
echo "  # Verify Ubuntu is installed"
echo "  wsl -l -v"
echo ""
echo "  # Open Ubuntu"
echo "  wsl -d Ubuntu"
echo ""
echo "Once inside Ubuntu, run:"
echo "  bash /path/to/rfing/mega_rebuild.sh"
