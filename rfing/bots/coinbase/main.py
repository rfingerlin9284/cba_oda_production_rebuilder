"""
main.py — Coinbase Crypto Algo Bot Entry Point
===============================================
Runs continuously, polling Coinbase Advanced Trade for new candle data and
executing trades according to the configured strategy.

Usage (from rfing/bots/coinbase/):
    source venv/bin/activate
    python main.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Dict

from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import CoinbaseConfig
from strategies import STRATEGY_MAP
from utils import CoinbaseClient, send_alert


def setup_logging(config: CoinbaseConfig) -> None:
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger.remove()
    logger.add(sys.stderr, level=config.LOG_LEVEL)
    logger.add(
        config.LOG_DIR / "coinbase_{time:YYYY-MM-DD}.log",
        level=config.LOG_LEVEL,
        rotation="00:00",
        retention="30 days",
        compression="zip",
    )


def run_cycle(
    client: CoinbaseClient,
    strategy,
    config: CoinbaseConfig,
    positions: Dict[str, float],
) -> None:
    """
    Execute one polling cycle across all configured products.

    Parameters
    ----------
    positions : dict mapping product_id -> base_size held (0.0 if flat)
    """
    try:
        usd_balance = client.get_usd_balance()
        logger.info(f"USD balance: {usd_balance:.2f}")
    except Exception as exc:
        logger.error(f"Failed to retrieve balance: {exc}")
        return

    for product_id in config.PRODUCTS:
        try:
            df = client.get_candles(product_id, config.GRANULARITY_SEC, config.CANDLE_COUNT)
            if df.empty:
                logger.warning(f"{product_id}: no candle data returned.")
                continue

            signal = strategy.generate_signal(df)
            current_price = df["close"].iloc[-1]
            held = positions.get(product_id, 0.0)
            logger.info(
                f"{product_id} | signal={signal} | close={current_price:.4f} | held={held:.8f}"
            )

            if signal == "BUY" and held == 0.0:
                # Only buy when flat (no existing position)
                order_size = min(config.ORDER_SIZE_QUOTE, usd_balance * config.MAX_RISK)
                if order_size < 1.0:
                    logger.warning(
                        f"{product_id}: insufficient balance to buy (${order_size:.2f})."
                    )
                    continue
                client.place_market_buy(product_id, order_size)
                # Estimate base units received (approximate; real value from fill)
                approx_base = order_size / current_price
                positions[product_id] = approx_base
                send_alert(f"[Coinbase] BUY {product_id} | ${order_size:.2f} (~{approx_base:.8f})")

            elif signal == "SELL" and held > 0.0:
                # Sell the entire tracked position
                client.place_market_sell(product_id, held)
                positions[product_id] = 0.0
                send_alert(f"[Coinbase] SELL {product_id} | {held:.8f} units")

        except Exception as exc:
            logger.error(f"{product_id}: error during cycle — {exc}")


def main() -> None:
    config = CoinbaseConfig()
    setup_logging(config)

    logger.info("─── Coinbase Crypto Bot starting ───")
    logger.info(f"Sandbox     : {config.SANDBOX}")
    logger.info(f"Strategy    : {config.STRATEGY}")
    logger.info(f"Products    : {config.PRODUCTS}")
    logger.info(f"Granularity : {config.GRANULARITY_SEC}s")

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
    client = CoinbaseClient(config)

    # In-memory position tracker: product_id -> base units held
    positions: Dict[str, float] = {p: 0.0 for p in config.PRODUCTS}

    logger.info(f"Polling every {config.POLL_INTERVAL_SEC}s. Press Ctrl+C to stop.")
    while True:
        run_cycle(client, strategy, config, positions)
        time.sleep(config.POLL_INTERVAL_SEC)


if __name__ == "__main__":
    main()
