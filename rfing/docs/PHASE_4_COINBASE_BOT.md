# Phase 4 — Coinbase Crypto Bot

> **Goal:** Configure, test, and run the Coinbase Advanced Trade crypto bot.

---

## 1. Get your Coinbase API credentials

1. Log in to [Coinbase Advanced Trade](https://advanced.coinbase.com/)
2. Go to **Settings → API** (or visit `https://www.coinbase.com/settings/api`)
3. Click **New API Key**
4. Enable permissions: **View**, **Trade**
5. Note your **API Key** and **API Secret**

> ⚠️ **Store these securely** — the secret is only shown once.

---

## 2. Configure your .env

```bash
nano ~/rfing/.env
```

Fill in:

```ini
COINBASE_API_KEY=your_api_key
COINBASE_API_SECRET=your_api_secret
COINBASE_SANDBOX=false          # set true for paper trading
```

---

## 3. Bot settings reference

| Variable | Default | Description |
|----------|---------|-------------|
| `COINBASE_PRODUCTS` | `BTC-USD,ETH-USD` | Comma-separated products to trade |
| `COINBASE_GRANULARITY_SEC` | `3600` | Candle size in seconds (60, 300, 900, 3600, 21600, 86400) |
| `COINBASE_CANDLE_COUNT` | `200` | Historical candles for indicators |
| `COINBASE_STRATEGY` | `ma_crossover` | `ma_crossover` or `rsi_mean_reversion` |
| `COINBASE_MA_FAST` | `20` | Fast EMA period |
| `COINBASE_MA_SLOW` | `50` | Slow EMA period |
| `COINBASE_RSI_PERIOD` | `14` | RSI period |
| `COINBASE_RSI_OVERSOLD` | `30` | RSI buy threshold |
| `COINBASE_RSI_OVERBOUGHT` | `70` | RSI sell threshold |
| `COINBASE_ORDER_SIZE_QUOTE` | `10.0` | Fixed USD amount per BUY order |
| `COINBASE_POLL_INTERVAL_SEC` | `3600` | Seconds between polling cycles |
| `MAX_RISK_PER_TRADE` | `0.01` | Max fraction of balance risked per trade |

---

## 4. Run the bot manually

```bash
cd ~/rfing/bots/coinbase
source venv/bin/activate
python main.py
```

---

## 5. Run in the background

```bash
cd ~/rfing
bash scripts/start_all.sh
bash scripts/status.sh
bash scripts/monitor.sh
```

---

## 6. Bot file structure

```
bots/coinbase/
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
    ├── coinbase_client.py     ← Advanced Trade API wrapper
    └── notifier.py            ← Telegram / email alerts
```

---

## ✅ Phase 4 Complete

Continue to **[Phase 5 — Production Checklist](PHASE_5_PRODUCTION.md)**.
