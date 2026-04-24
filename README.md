# CBA_ODA Production Rebuilder

> **Complete, reproducible backup and rebuild system for the OANDA Forex and
> Coinbase Crypto algorithmic trading bots.**  
> Download → Unzip → Double-click `install.bat` → Done.

---

## ⚡ Quick Start (Windows + WSL)

1. **Download** this repository as a ZIP from GitHub  
   *(Code → Download ZIP)*
2. **Unzip** the folder anywhere on your Windows machine
3. **Open the `rfing/` folder** inside the unzipped archive
4. **Double-click `install.bat`**  
   *(This opens Ubuntu WSL and installs everything automatically)*
5. When installation completes, **add your API keys**:
   ```bash
   nano ~/rfing/.env
   ```
6. **Start both bots**:
   ```bash
   cd ~/rfing
   bash scripts/start_all.sh
   ```

---

## 📋 What's included

| Component | Location | Description |
|-----------|----------|-------------|
| **install.bat** | `rfing/install.bat` | Windows double-click installer — launches WSL Ubuntu and runs the mega script |
| **mega_rebuild.sh** | `rfing/mega_rebuild.sh` | Master rebuild script — installs all dependencies from scratch |
| **OANDA Forex Bot** | `rfing/bots/oanda/` | Algo trading bot for OANDA forex (EUR/USD, GBP/USD, USD/JPY …) |
| **Coinbase Crypto Bot** | `rfing/bots/coinbase/` | Algo trading bot for Coinbase Advanced Trade (BTC-USD, ETH-USD …) |
| **Phase Docs** | `rfing/docs/` | Step-by-step installation and configuration guides |
| **Operational Scripts** | `rfing/scripts/` | Start, stop, monitor, and status helpers |
| **Setup Scripts** | `rfing/setup/` | Individual phase setup scripts |

---

## 📁 Project Structure

```
rfing/                          ← root project folder
├── install.bat                 ← Windows double-click installer
├── mega_rebuild.sh             ← master rebuild script (run inside Ubuntu)
├── .env.example                ← copy to .env and fill in API keys
│
├── bots/
│   ├── oanda/                  ← OANDA Forex Bot
│   │   ├── main.py             ← entry point
│   │   ├── config.py           ← configuration loader
│   │   ├── requirements.txt    ← Python dependencies
│   │   ├── strategies/         ← trading strategies (EMA crossover, RSI)
│   │   └── utils/              ← API client, position sizer, alerts
│   │
│   └── coinbase/               ← Coinbase Crypto Bot
│       ├── main.py
│       ├── config.py
│       ├── requirements.txt
│       ├── strategies/
│       └── utils/
│
├── docs/
│   ├── PHASE_1_WSL_SETUP.md    ← Enable WSL + install Ubuntu
│   ├── PHASE_2_ENVIRONMENT.md  ← Run the installer
│   ├── PHASE_3_OANDA_BOT.md    ← OANDA bot config & usage
│   ├── PHASE_4_COINBASE_BOT.md ← Coinbase bot config & usage
│   ├── PHASE_5_PRODUCTION.md   ← Production checklist
│   └── TROUBLESHOOTING.md      ← Common issues & fixes
│
├── scripts/
│   ├── start_all.sh            ← start both bots in background
│   ├── stop_all.sh             ← stop both bots
│   ├── status.sh               ← check running status
│   └── monitor.sh              ← tail live logs (tmux split view)
│
├── setup/
│   ├── 01_wsl_ubuntu.sh        ← WSL setup reference
│   ├── 02_system_packages.sh   ← APT packages
│   ├── 03_oanda_env.sh         ← OANDA Python venv
│   ├── 04_coinbase_env.sh      ← Coinbase Python venv
│   └── 05_configure.sh         ← interactive API key setup
│
└── logs/                       ← bot log files (auto-created)
```

---

## 📖 Phase-by-Phase Guides

| Phase | Guide | Topic |
|-------|-------|-------|
| 1 | [PHASE_1_WSL_SETUP.md](rfing/docs/PHASE_1_WSL_SETUP.md) | Enable WSL 2 + install Ubuntu on Windows |
| 2 | [PHASE_2_ENVIRONMENT.md](rfing/docs/PHASE_2_ENVIRONMENT.md) | Run the mega installer |
| 3 | [PHASE_3_OANDA_BOT.md](rfing/docs/PHASE_3_OANDA_BOT.md) | OANDA forex bot setup |
| 4 | [PHASE_4_COINBASE_BOT.md](rfing/docs/PHASE_4_COINBASE_BOT.md) | Coinbase crypto bot setup |
| 5 | [PHASE_5_PRODUCTION.md](rfing/docs/PHASE_5_PRODUCTION.md) | Pre-launch production checklist |
| — | [TROUBLESHOOTING.md](rfing/docs/TROUBLESHOOTING.md) | Common problems and solutions |

---

## 🤖 Trading Strategies

Both bots support two built-in strategies, switchable via `.env`:

### Moving Average Crossover (`ma_crossover`)
- **BUY** when the fast EMA crosses above the slow EMA
- **SELL** when the fast EMA crosses below the slow EMA
- Best for trending markets

### RSI Mean Reversion (`rsi_mean_reversion`)
- **BUY** when RSI recovers from oversold territory (<30)
- **SELL** when RSI falls back from overbought territory (>70)
- Best for ranging markets

---

## 🔑 API Keys Required

| Bot | Provider | Credentials needed |
|-----|----------|--------------------|
| OANDA | [oanda.com](https://www.oanda.com/) | API Key + Account ID |
| Coinbase | [coinbase.com/settings/api](https://www.coinbase.com/settings/api) | API Key + API Secret |

> Start with **practice / paper** accounts — never risk real money until the
> bot has been tested and you understand the risk.

---

## ⚠️ Risk Disclaimer

This software is provided for **educational and research purposes**.  
Algorithmic trading carries significant financial risk.  
Past performance does not guarantee future results.  
You are solely responsible for any trades executed by this software.  
Always test in a practice environment before using real funds.

---

## 📄 License

MIT — see [LICENSE](LICENSE)
