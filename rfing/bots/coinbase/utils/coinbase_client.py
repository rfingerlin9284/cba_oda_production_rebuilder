"""
utils/coinbase_client.py — Wrapper around the Coinbase Advanced Trade API
Uses the official coinbase-advanced-py SDK.
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta

import pandas as pd
from loguru import logger
from coinbase.rest import RESTClient


# Granularity label map: seconds -> Coinbase API string
_GRAN_MAP: dict[int, str] = {
    60:    "ONE_MINUTE",
    300:   "FIVE_MINUTE",
    900:   "FIFTEEN_MINUTE",
    3600:  "ONE_HOUR",
    21600: "SIX_HOUR",
    86400: "ONE_DAY",
}


class CoinbaseClient:
    """Encapsulates all Coinbase Advanced Trade API calls used by the bot."""

    def __init__(self, config) -> None:
        self.config = config
        self.client = RESTClient(
            api_key=config.API_KEY,
            api_secret=config.API_SECRET,
        )

    # ── Account ───────────────────────────────────────────────────────────────
    def get_usd_balance(self) -> float:
        """Return available USD cash balance."""
        response = self.client.get_accounts()
        for account in response.get("accounts", []):
            if account.get("currency") == "USD":
                return float(account["available_balance"]["value"])
        return 0.0

    # ── Market data ───────────────────────────────────────────────────────────
    def get_candles(self, product_id: str, granularity_sec: int, count: int) -> pd.DataFrame:
        """Fetch historical OHLCV candles and return as a DataFrame."""
        gran_str = _GRAN_MAP.get(granularity_sec, "ONE_HOUR")
        end = datetime.now(timezone.utc)
        start = end - timedelta(seconds=granularity_sec * count)

        response = self.client.get_candles(
            product_id=product_id,
            start=int(start.timestamp()),
            end=int(end.timestamp()),
            granularity=gran_str,
        )

        rows = []
        for c in response.get("candles", []):
            rows.append({
                "time":   pd.Timestamp(int(c["start"]), unit="s", tz="UTC"),
                "open":   float(c["open"]),
                "high":   float(c["high"]),
                "low":    float(c["low"]),
                "close":  float(c["close"]),
                "volume": float(c["volume"]),
            })

        df = pd.DataFrame(rows).set_index("time").sort_index()
        return df

    # ── Orders ────────────────────────────────────────────────────────────────
    def place_market_buy(self, product_id: str, quote_size: float) -> dict:
        """Buy `quote_size` USD worth of `product_id`."""
        import uuid
        order_id = str(uuid.uuid4())
        response = self.client.market_order_buy(
            client_order_id=order_id,
            product_id=product_id,
            quote_size=str(round(quote_size, 2)),
        )
        logger.info(f"Market BUY | {product_id} | quote_size={quote_size} | {response}")
        return response

    def place_market_sell(self, product_id: str, base_size: float) -> dict:
        """Sell `base_size` units of the base currency in `product_id`."""
        import uuid
        order_id = str(uuid.uuid4())
        response = self.client.market_order_sell(
            client_order_id=order_id,
            product_id=product_id,
            base_size=str(round(base_size, 8)),
        )
        logger.info(f"Market SELL | {product_id} | base_size={base_size} | {response}")
        return response
