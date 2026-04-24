#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════════════════
#  setup/05_configure.sh
#  Interactive helper to fill in ~/rfing/.env with API credentials.
# ════════════════════════════════════════════════════════════════════════════════
set -euo pipefail

RFING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$RFING_DIR/.env"

if [ ! -f "$ENV_FILE" ]; then
    cp "$RFING_DIR/.env.example" "$ENV_FILE"
fi

echo ""
echo "══ API Credential Configuration ══"
echo "  Edit: $ENV_FILE"
echo ""
echo "  You will need:"
echo "    - OANDA API Key and Account ID (from https://www.oanda.com/)"
echo "    - Coinbase Advanced Trade API Key and Secret (from https://www.coinbase.com/settings/api)"
echo ""

# ── OANDA ─────────────────────────────────────────────────────────────────────
read -rp "Enter OANDA_API_KEY      : " oda_key
read -rp "Enter OANDA_ACCOUNT_ID   : " oda_acct
read -rp "OANDA environment [practice/live] (default: practice): " oda_env
oda_env="${oda_env:-practice}"

# ── Coinbase ──────────────────────────────────────────────────────────────────
read -rp "Enter COINBASE_API_KEY    : " cb_key
read -rsp "Enter COINBASE_API_SECRET : " cb_secret
echo

# ── Write to .env ─────────────────────────────────────────────────────────────
sed -i "s|^OANDA_API_KEY=.*|OANDA_API_KEY=$oda_key|"         "$ENV_FILE"
sed -i "s|^OANDA_ACCOUNT_ID=.*|OANDA_ACCOUNT_ID=$oda_acct|" "$ENV_FILE"
sed -i "s|^OANDA_ENVIRONMENT=.*|OANDA_ENVIRONMENT=$oda_env|" "$ENV_FILE"
sed -i "s|^COINBASE_API_KEY=.*|COINBASE_API_KEY=$cb_key|"   "$ENV_FILE"
sed -i "s|^COINBASE_API_SECRET=.*|COINBASE_API_SECRET=$cb_secret|" "$ENV_FILE"

echo ""
echo "[OK] .env updated. Review it with: nano $ENV_FILE"
echo ""
