# Phase 1 — Windows WSL Ubuntu Setup

> **Goal:** Get a clean Ubuntu environment running inside Windows Subsystem for
> Linux (WSL 2), ready to install the bots.

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Windows 10 (build 19041+) or Windows 11 | Run `winver` to check |
| Administrator access | Needed to enable WSL |
| 8 GB RAM minimum | 16 GB recommended |
| 20 GB free disk space | For Ubuntu + Python deps |

---

## Step 1 — Enable WSL 2 (PowerShell as Administrator)

Open **PowerShell** with *Run as Administrator* and paste:

```powershell
# Enable WSL and install Ubuntu in one command (Windows 11 / recent Win 10)
wsl --install

# Set WSL 2 as the default version
wsl --set-default-version 2
```

**Restart your computer** when prompted.

---

## Step 2 — First-time Ubuntu setup

After reboot, Ubuntu will launch automatically and ask you to create a UNIX
username and password.  Use something simple like `rfing`:

```
Enter new UNIX username: rfing
New password: ••••••••
Retype new password: ••••••••
```

---

## Step 3 — Verify WSL is working

In PowerShell:

```powershell
wsl -l -v
```

Expected output:

```
  NAME      STATE           VERSION
* Ubuntu    Running         2
```

---

## Step 4 — Open Ubuntu terminal

You can open Ubuntu any time from:
- **Start Menu** → search "Ubuntu"
- **Windows Terminal** → click the `∨` dropdown → Ubuntu
- **PowerShell** → type `wsl`

---

## Step 5 — Update Ubuntu packages (inside Ubuntu)

```bash
sudo apt update && sudo apt upgrade -y
```

---

## ✅ Phase 1 Complete

Your Ubuntu WSL environment is ready.  
Continue to **[Phase 2 — Environment Setup](PHASE_2_ENVIRONMENT.md)**.
