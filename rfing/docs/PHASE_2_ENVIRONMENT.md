# Phase 2 — Environment Setup

> **Goal:** Clone / unzip the project into `~/rfing`, install system packages,
> and run the mega-rebuild script that sets up everything automatically.

---

## Option A — One-click install from Windows (recommended)

1. Download and unzip the repository anywhere on your Windows machine  
   (e.g. `C:\Users\rfing\Downloads\rfing`)
2. Inside the unzipped folder, **double-click `install.bat`**
3. A WSL terminal will open and run the full installation automatically
4. Follow any on-screen prompts (may ask for your WSL `sudo` password)

> The script copies the project into `~/rfing` inside Ubuntu and runs
> `mega_rebuild.sh` for you.

---

## Option B — Manual setup inside Ubuntu

```bash
# 1. Copy the project into your Ubuntu home directory
#    (from inside Ubuntu — adjust the Windows path as needed)
cp -r /mnt/c/Users/rfing/Downloads/rfing ~/rfing

# 2. Enter the project folder
cd ~/rfing

# 3. Run the master installation script
bash mega_rebuild.sh
```

---

## What the mega_rebuild.sh script does

| Phase | Action |
|-------|--------|
| 1 | APT update + install system packages (Python 3, git, tmux …) |
| 2 | Copy / sync project files into `~/rfing` |
| 3 | Create Python virtual env for OANDA bot + install packages |
| 4 | Create Python virtual env for Coinbase bot + install packages |
| 5 | Set executable permissions on all scripts |
| 6 | Run import smoke-tests to verify the install |

Total install time: **3–10 minutes** depending on internet speed.

---

## After installation

Your `~/rfing` directory will look like:

```
~/rfing/
├── .env                  ← fill in your API keys here
├── mega_rebuild.sh
├── install.bat
├── bots/
│   ├── oanda/            ← OANDA forex bot
│   └── coinbase/         ← Coinbase crypto bot
├── docs/                 ← these phase guides
├── scripts/              ← start / stop / monitor helpers
└── logs/                 ← live log output
```

---

## ✅ Phase 2 Complete

Continue to **[Phase 3 — OANDA Bot Configuration](PHASE_3_OANDA_BOT.md)**.
