# Phase 5 — Production Checklist

> **Goal:** Complete all steps before trading with real money.

---

## Pre-flight checklist

### Security
- [ ] `.env` file exists at `~/rfing/.env` and is **not** committed to git
  ```bash
  cat ~/rfing/.gitignore | grep .env   # should show ".env"
  git -C ~/rfing status                # should NOT show .env as a tracked file
  ```
- [ ] API keys have **minimum required permissions** (no withdrawal permission)
- [ ] OANDA key is scoped to a single account
- [ ] Coinbase key does NOT have transfer/withdrawal permissions
- [ ] `~/rfing` directory permissions are owner-only:
  ```bash
  chmod 700 ~/rfing
  chmod 600 ~/rfing/.env
  ```

---

### OANDA Bot
- [ ] Successfully ran in **practice mode** for at least 48 hours
- [ ] Logs show correct candle data being fetched
- [ ] At least one trade executed correctly in practice mode
- [ ] `OANDA_ENVIRONMENT=practice` → changed to `live` only when ready
- [ ] Position sizing (`MAX_RISK_PER_TRADE`) reviewed and acceptable

---

### Coinbase Bot
- [ ] API key tested with `COINBASE_SANDBOX=false` in practice
- [ ] At least one small test BUY order placed and confirmed in Coinbase UI
- [ ] `COINBASE_ORDER_SIZE_QUOTE` set to a comfortable amount (start small, e.g. `10.0`)

---

### Monitoring
- [ ] Logs rotating daily under `~/rfing/logs/`
- [ ] Optional: Telegram alerts configured and tested (send a test message)
- [ ] Bot restarts automatically after a crash (see optional systemd section below)

---

## Optional: Auto-restart with systemd (WSL 2)

Create service files to restart bots if they crash:

```bash
# OANDA bot service
sudo tee /etc/systemd/system/oanda-bot.service > /dev/null << 'EOF'
[Unit]
Description=OANDA Forex Algo Bot
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/rfing/bots/oanda
ExecStart=/home/YOUR_USERNAME/rfing/bots/oanda/venv/bin/python main.py
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
EOF

# Coinbase bot service
sudo tee /etc/systemd/system/coinbase-bot.service > /dev/null << 'EOF'
[Unit]
Description=Coinbase Crypto Algo Bot
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/rfing/bots/coinbase
ExecStart=/home/YOUR_USERNAME/rfing/bots/coinbase/venv/bin/python main.py
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable oanda-bot coinbase-bot
sudo systemctl start  oanda-bot coinbase-bot
sudo systemctl status oanda-bot coinbase-bot
```

---

## Routine maintenance

| Task | Command | Frequency |
|------|---------|-----------|
| Check bot status | `bash ~/rfing/scripts/status.sh` | Daily |
| View logs | `bash ~/rfing/scripts/monitor.sh` | As needed |
| Restart all bots | `bash ~/rfing/scripts/stop_all.sh && bash ~/rfing/scripts/start_all.sh` | As needed |
| Update dependencies | `cd bots/oanda && source venv/bin/activate && pip install -r requirements.txt --upgrade` | Monthly |
| Full rebuild from zip | `bash mega_rebuild.sh` | After any system reinstall |

---

## ✅ Production ready

Both bots are configured, tested, and running.  
See **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** if you encounter any issues.
