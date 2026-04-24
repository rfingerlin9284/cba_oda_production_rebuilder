"""
config.py — Coinbase Bot Configuration
Loads all settings from the shared ~/rfing/.env file.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parents[2]   # rfing/
load_dotenv(_ROOT / ".env")


class CoinbaseConfig:
    # ── API credentials ──────────────────────────────────────────────────────
    API_KEY: str = os.getenv("COINBASE_API_KEY", "")
    API_SECRET: str = os.getenv("COINBASE_API_SECRET", "")
    SANDBOX: bool = os.getenv("COINBASE_SANDBOX", "false").lower() == "true"

    # ── Trading parameters ───────────────────────────────────────────────────
    # Products to trade (Coinbase product IDs, e.g. "BTC-USD")
    PRODUCTS: list[str] = [
        p.strip()
        for p in os.getenv("COINBASE_PRODUCTS", "BTC-USD,ETH-USD").split(",")
        if p.strip()
    ]

    # Candle granularity in seconds: 60 300 900 3600 21600 86400
    GRANULARITY_SEC: int = int(os.getenv("COINBASE_GRANULARITY_SEC", "3600"))

    # Number of historical candles to fetch for indicator calculation
    CANDLE_COUNT: int = int(os.getenv("COINBASE_CANDLE_COUNT", "200"))

    # Strategy: "ma_crossover" | "rsi_mean_reversion"
    STRATEGY: str = os.getenv("COINBASE_STRATEGY", "ma_crossover")

    # Maximum risk per trade as fraction of balance (default 1 %)
    MAX_RISK: float = float(os.getenv("MAX_RISK_PER_TRADE", "0.01"))

    # ── MA Crossover parameters ──────────────────────────────────────────────
    MA_FAST: int = int(os.getenv("COINBASE_MA_FAST", "20"))
    MA_SLOW: int = int(os.getenv("COINBASE_MA_SLOW", "50"))

    # ── RSI Mean Reversion parameters ───────────────────────────────────────
    RSI_PERIOD: int = int(os.getenv("COINBASE_RSI_PERIOD", "14"))
    RSI_OVERSOLD: float = float(os.getenv("COINBASE_RSI_OVERSOLD", "30"))
    RSI_OVERBOUGHT: float = float(os.getenv("COINBASE_RSI_OVERBOUGHT", "70"))

    # ── Order sizing ─────────────────────────────────────────────────────────
    # Quote currency order size (e.g. 10.00 USD per trade)
    ORDER_SIZE_QUOTE: float = float(os.getenv("COINBASE_ORDER_SIZE_QUOTE", "10.0"))

    # ── Loop / scheduling ────────────────────────────────────────────────────
    POLL_INTERVAL_SEC: int = int(os.getenv("COINBASE_POLL_INTERVAL_SEC", "3600"))

    # ── Logging ──────────────────────────────────────────────────────────────
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR: Path = Path(os.getenv("LOG_DIR", str(_ROOT / "logs")))

    # ── Validation ───────────────────────────────────────────────────────────
    @classmethod
    def validate(cls) -> None:
        missing = [f for f in ("API_KEY", "API_SECRET") if not getattr(cls, f)]
        if missing:
            raise EnvironmentError(
                f"Missing required Coinbase env vars: {', '.join('COINBASE_' + f for f in missing)}. "
                f"Edit ~/rfing/.env and fill in your credentials."
            )
