# Phase 3 — OANDA Forex Bot

> **Goal:** Configure, test, and run the OANDA forex algorithmic trading bot.

---

## 1. Get your OANDA API credentials

1. Log in to [OANDA](https://www.oanda.com/) (or create a free Practice account)
2. Go to **My Account → Manage API Access**
3. Generate a new **Personal Access Token**
4. Note your **Account ID** (shown on the dashboard)

---

## 2. Configure your .env

Open the environment file:

```bash
nano ~/rfing/.env
```

Fill in:

```ini
OANDA_API_KEY=your_personal_access_token
OANDA_ACCOUNT_ID=your_account_id
OANDA_ENVIRONMENT=practice     # change to "live" only when ready for real money
```

Save and exit (`Ctrl+X`, `Y`, `Enter`).

---

## 3. Bot settings reference

| Variable | Default | Description |
|----------|---------|-------------|
| `OANDA_INSTRUMENTS` | `EUR_USD,GBP_USD,USD_JPY` | Comma-separated instruments to trade |
| `OANDA_GRANULARITY` | `H1` | Candle timeframe (M5, M15, H1, H4, D …) |
| `OANDA_CANDLE_COUNT` | `200` | Historical candles to load |
| `OANDA_STRATEGY` | `ma_crossover` | `ma_crossover` or `rsi_mean_reversion` |
| `OANDA_MA_FAST` | `20` | Fast EMA period (MA crossover strategy) |
| `OANDA_MA_SLOW` | `50` | Slow EMA period (MA crossover strategy) |
| `OANDA_RSI_PERIOD` | `14` | RSI look-back period |
| `OANDA_RSI_OVERSOLD` | `30` | RSI buy threshold |
| `OANDA_RSI_OVERBOUGHT` | `70` | RSI sell threshold |
| `OANDA_POLL_INTERVAL_SEC` | `3600` | Seconds between each polling cycle |
| `MAX_RISK_PER_TRADE` | `0.01` | Risk per trade as fraction of balance (1%) |

---

## 4. Run the bot manually (recommended first)

```bash
cd ~/rfing/bots/oanda
source venv/bin/activate
python main.py
```

Watch the log output.  Press `Ctrl+C` to stop.

---

## 5. Run in the background

```bash
cd ~/rfing
bash scripts/start_all.sh    # starts both bots in background
bash scripts/status.sh       # check running status
bash scripts/monitor.sh      # tail live logs
```

---

## 6. Available strategies

### MA Crossover (`ma_crossover`)
- **BUY** when the fast EMA crosses **above** the slow EMA
- **SELL** when the fast EMA crosses **below** the slow EMA
- Good for trending markets

### RSI Mean Reversion (`rsi_mean_reversion`)
- **BUY** when RSI crosses back up through the oversold threshold
- **SELL** when RSI crosses back down through the overbought threshold
- Good for ranging markets

---

## 7. Bot file structure

```
bots/oanda/
├── main.py                    ← entry point
├── config.py                  ← loads .env settings
├── requirements.txt           ← Python dependencies
├── strategies/
│   ├── __init__.py
│   ├── base_strategy.py       ← abstract base class
│   ├── ma_crossover.py        ← EMA crossover strategy
│   └── rsi_mean_reversion.py  ← RSI strategy
└── utils/
    ├── __init__.py
    ├── oanda_client.py        ← API wrapper
    ├── position_sizer.py      ← risk-based unit calculator
    └── notifier.py            ← Telegram / email alerts
```

---

## ✅ Phase 3 Complete

Continue to **[Phase 4 — Coinbase Bot Configuration](PHASE_4_COINBASE_BOT.md)**.
