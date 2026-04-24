"""
config.py — OANDA Bot Configuration
Loads all settings from the shared ~/rfing/.env file.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Walk up from this file to the rfing root and load .env
_ROOT = Path(__file__).resolve().parents[2]   # rfing/
load_dotenv(_ROOT / ".env")


class OandaConfig:
    # ── API credentials ──────────────────────────────────────────────────────
    API_KEY: str = os.getenv("OANDA_API_KEY", "")
    ACCOUNT_ID: str = os.getenv("OANDA_ACCOUNT_ID", "")
    ENVIRONMENT: str = os.getenv("OANDA_ENVIRONMENT", "practice")   # practice | live

    # ── Trading parameters ───────────────────────────────────────────────────
    # Instruments to trade (OANDA format, e.g. "EUR_USD")
    INSTRUMENTS: list[str] = [
        i.strip()
        for i in os.getenv("OANDA_INSTRUMENTS", "EUR_USD,GBP_USD,USD_JPY").split(",")
        if i.strip()
    ]

    # Candle granularity: S5 S10 S15 S30 M1 M2 M4 M5 M10 M15 M30 H1 H2 H3 H4 H6 H8 H12 D W M
    GRANULARITY: str = os.getenv("OANDA_GRANULARITY", "H1")

    # Number of historical candles to load for indicator calculation
    CANDLE_COUNT: int = int(os.getenv("OANDA_CANDLE_COUNT", "200"))

    # Maximum risk per trade as fraction of account balance (default 1 %)
    MAX_RISK: float = float(os.getenv("MAX_RISK_PER_TRADE", "0.01"))

    # Strategy to run: "ma_crossover" | "rsi_mean_reversion"
    STRATEGY: str = os.getenv("OANDA_STRATEGY", "ma_crossover")

    # ── MA Crossover parameters ──────────────────────────────────────────────
    MA_FAST: int = int(os.getenv("OANDA_MA_FAST", "20"))
    MA_SLOW: int = int(os.getenv("OANDA_MA_SLOW", "50"))

    # ── RSI Mean Reversion parameters ───────────────────────────────────────
    RSI_PERIOD: int = int(os.getenv("OANDA_RSI_PERIOD", "14"))
    RSI_OVERSOLD: float = float(os.getenv("OANDA_RSI_OVERSOLD", "30"))
    RSI_OVERBOUGHT: float = float(os.getenv("OANDA_RSI_OVERBOUGHT", "70"))

    # ── Stop-loss distance (pips) for position sizing ────────────────────────
    STOP_LOSS_PIPS: int = int(os.getenv("OANDA_STOP_LOSS_PIPS", "10"))

    # ── Loop / scheduling ────────────────────────────────────────────────────
    # Seconds between each polling cycle (use 60 for M1, 3600 for H1, etc.)
    POLL_INTERVAL_SEC: int = int(os.getenv("OANDA_POLL_INTERVAL_SEC", "3600"))

    # ── Logging ──────────────────────────────────────────────────────────────
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR: Path = Path(os.getenv("LOG_DIR", str(_ROOT / "logs")))

    # ── Validation ───────────────────────────────────────────────────────────
    @classmethod
    def validate(cls) -> None:
        missing = [f for f in ("API_KEY", "ACCOUNT_ID") if not getattr(cls, f)]
        if missing:
            raise EnvironmentError(
                f"Missing required OANDA env vars: {', '.join('OANDA_' + f for f in missing)}. "
                f"Edit ~/rfing/.env and fill in your credentials."
            )
