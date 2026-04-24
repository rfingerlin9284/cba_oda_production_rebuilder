# Troubleshooting Guide

---

## WSL / Ubuntu Issues

### WSL command not found (Windows)
```
'wsl' is not recognized as an internal or external command
```
**Fix:** Open PowerShell as Administrator and run:
```powershell
wsl --install
```
Then restart your computer.

---

### Ubuntu distribution missing
```
There is no distribution with the supplied name.
```
**Fix:** Install Ubuntu from the Microsoft Store:
[https://aka.ms/wslubuntu](https://aka.ms/wslubuntu)

---

### Permission denied running .sh scripts
```
bash: ./mega_rebuild.sh: Permission denied
```
**Fix:**
```bash
chmod +x ~/rfing/mega_rebuild.sh
chmod +x ~/rfing/scripts/*.sh
chmod +x ~/rfing/setup/*.sh
```

---

## Python / pip Issues

### `python3` not found
**Fix:**
```bash
sudo apt-get install python3 python3-pip python3-venv
```

### pip install fails with SSL error
**Fix:**
```bash
sudo apt-get install ca-certificates libssl-dev
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### `ModuleNotFoundError` when running a bot
**Fix:** Make sure you activated the virtual environment first:
```bash
cd ~/rfing/bots/oanda    # or coinbase
source venv/bin/activate
python main.py
```

---

## OANDA Bot Issues

### `V20Error: [401]` — Unauthorized
**Cause:** Invalid API key.  
**Fix:** Double-check `OANDA_API_KEY` in `~/rfing/.env`.  
Generate a new token at: https://www.oanda.com/account/profile/api_access

### `V20Error: [404]` — Account not found
**Cause:** Wrong account ID or wrong environment (practice vs live).  
**Fix:** Check `OANDA_ACCOUNT_ID` and `OANDA_ENVIRONMENT` in `.env`.

### No trades executing (always HOLD)
**Cause:** Not enough data or signal never triggers.  
**Fix:**
- Reduce `OANDA_MA_FAST` / `OANDA_MA_SLOW` for more frequent signals
- Lower `OANDA_GRANULARITY` (e.g. `M15` instead of `H1`) for more candles per day
- Try the `rsi_mean_reversion` strategy instead

---

## Coinbase Bot Issues

### `AuthenticationError` — Invalid API key
**Fix:** Regenerate API key at https://www.coinbase.com/settings/api  
Ensure the key has **View** and **Trade** permissions.

### `InsufficientFundsError`
**Fix:** Reduce `COINBASE_ORDER_SIZE_QUOTE` in `.env` to match your balance.

### Candle data returns empty DataFrame
**Cause:** Product may be delisted or granularity value is invalid.  
**Fix:** Use one of the supported granularities: `60, 300, 900, 3600, 21600, 86400`

---

## Log Issues

### Logs not appearing
**Fix:**
```bash
ls -la ~/rfing/logs/
# If empty, check the bot is actually running:
bash ~/rfing/scripts/status.sh
```

### Log file growing too large
**Fix:** Logs rotate daily and compress automatically (via loguru `rotation`).  
Check retention setting in `main.py` — default is 30 days.

---

## Full Reset / Reinstall

If something is broken beyond repair, run a full rebuild from the zip:

```bash
# Stop all bots first
bash ~/rfing/scripts/stop_all.sh

# Remove the virtual environments (keeps your .env)
rm -rf ~/rfing/bots/oanda/venv ~/rfing/bots/coinbase/venv

# Re-run the installer
bash ~/rfing/mega_rebuild.sh
```

---

## Getting Help

- OANDA v20 API docs: https://developer.oanda.com/rest-live-v20/introduction/
- Coinbase Advanced Trade API docs: https://docs.cdp.coinbase.com/advanced-trade/docs/welcome/
- oandapyV20 library: https://github.com/hootnot/oanda-api-v20
- coinbase-advanced-py library: https://github.com/coinbase/coinbase-advanced-py
