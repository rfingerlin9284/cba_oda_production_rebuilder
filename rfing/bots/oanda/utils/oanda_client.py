"""
utils/oanda_client.py — Thin wrapper around oandapyV20 REST API
"""
from __future__ import annotations

import pandas as pd
from loguru import logger
import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.positions as positions


class OandaClient:
    """Encapsulates all OANDA API calls used by the bot."""

    def __init__(self, config) -> None:
        self.config = config
        environment = "live" if config.ENVIRONMENT == "live" else "practice"
        self.api = oandapyV20.API(
            access_token=config.API_KEY,
            environment=environment,
        )
        self.account_id = config.ACCOUNT_ID

    # ── Account ───────────────────────────────────────────────────────────────
    def get_balance(self) -> float:
        """Return the current NAV of the account."""
        r = accounts.AccountSummary(self.account_id)
        self.api.request(r)
        return float(r.response["account"]["NAV"])

    # ── Market data ───────────────────────────────────────────────────────────
    def get_candles(self, instrument: str, granularity: str, count: int) -> pd.DataFrame:
        """Fetch OHLCV candles and return as a DataFrame."""
        params = {
            "count": count,
            "granularity": granularity,
            "price": "M",   # mid prices
        }
        r = instruments.InstrumentsCandles(instrument, params=params)
        self.api.request(r)

        rows = []
        for c in r.response["candles"]:
            if c["complete"]:
                mid = c["mid"]
                rows.append({
                    "time":   pd.Timestamp(c["time"]),
                    "open":   float(mid["o"]),
                    "high":   float(mid["h"]),
                    "low":    float(mid["l"]),
                    "close":  float(mid["c"]),
                    "volume": int(c["volume"]),
                })

        df = pd.DataFrame(rows).set_index("time").sort_index()
        return df

    # ── Orders ────────────────────────────────────────────────────────────────
    def place_market_order(self, instrument: str, units: int) -> dict:
        """
        Place a market order.

        Parameters
        ----------
        instrument : str  e.g. "EUR_USD"
        units      : int  positive = buy, negative = sell
        """
        data = {
            "order": {
                "type": "MARKET",
                "instrument": instrument,
                "units": str(units),
                "timeInForce": "FOK",
                "positionFill": "DEFAULT",
            }
        }
        r = orders.OrderCreate(self.account_id, data=data)
        self.api.request(r)
        logger.info(f"Order placed | {instrument} | units={units} | resp={r.response}")
        return r.response

    def close_position(self, instrument: str) -> dict:
        """Close the entire open position for the given instrument."""
        data = {"longUnits": "ALL", "shortUnits": "ALL"}
        r = positions.PositionClose(self.account_id, instrument, data=data)
        self.api.request(r)
        logger.info(f"Position closed | {instrument}")
        return r.response
