"""
main.py — OANDA Forex Algo Bot Entry Point
==========================================
Runs continuously, polling OANDA for new candle data and executing trades
according to the configured strategy.

Usage (from rfing/bots/oanda/):
    source venv/bin/activate
    python main.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

from loguru import logger

# ── ensure package is importable whether run directly or via script ────────────
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import OandaConfig
from strategies import STRATEGY_MAP
from utils import OandaClient, compute_units, send_alert


def setup_logging(config: OandaConfig) -> None:
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger.remove()
    logger.add(sys.stderr, level=config.LOG_LEVEL)
    logger.add(
        config.LOG_DIR / "oanda_{time:YYYY-MM-DD}.log",
        level=config.LOG_LEVEL,
        rotation="00:00",
        retention="30 days",
        compression="zip",
    )


def run_cycle(client: OandaClient, strategy, config: OandaConfig) -> None:
    """Execute one polling cycle across all configured instruments."""
    try:
        balance = client.get_balance()
        logger.info(f"Account NAV: {balance:.2f}")
    except Exception as exc:
        logger.error(f"Failed to retrieve account balance: {exc}")
        return

    for instrument in config.INSTRUMENTS:
        try:
            df = client.get_candles(instrument, config.GRANULARITY, config.CANDLE_COUNT)
            if df.empty:
                logger.warning(f"{instrument}: no candle data returned.")
                continue

            signal = strategy.generate_signal(df)
            logger.info(f"{instrument} | signal={signal} | last_close={df['close'].iloc[-1]:.5f}")

            if signal == "HOLD":
                continue

            # Simple position sizing: configured risk fraction and stop-loss pips
            units = compute_units(
                balance=balance,
                risk_fraction=config.MAX_RISK,
                stop_pips=config.STOP_LOSS_PIPS,
            )
            if signal == "SELL":
                units = -units

            client.place_market_order(instrument, units)
            msg = f"[OANDA] {signal} {instrument} | units={units} | NAV={balance:.2f}"
            send_alert(msg)

        except Exception as exc:
            logger.error(f"{instrument}: error during cycle — {exc}")


def main() -> None:
    config = OandaConfig()
    setup_logging(config)

    logger.info("─── OANDA Forex Bot starting ───")
    logger.info(f"Environment : {config.ENVIRONMENT}")
    logger.info(f"Strategy    : {config.STRATEGY}")
    logger.info(f"Instruments : {config.INSTRUMENTS}")
    logger.info(f"Granularity : {config.GRANULARITY}")

    try:
        config.validate()
    except EnvironmentError as exc:
        logger.critical(str(exc))
        sys.exit(1)

    StrategyClass = STRATEGY_MAP.get(config.STRATEGY)
    if StrategyClass is None:
        logger.critical(
            f"Unknown strategy '{config.STRATEGY}'. "
            f"Available: {list(STRATEGY_MAP.keys())}"
        )
        sys.exit(1)

    strategy = StrategyClass(config)
    client = OandaClient(config)

    logger.info(f"Polling every {config.POLL_INTERVAL_SEC}s. Press Ctrl+C to stop.")
    while True:
        run_cycle(client, strategy, config)
        time.sleep(config.POLL_INTERVAL_SEC)


if __name__ == "__main__":
    main()
