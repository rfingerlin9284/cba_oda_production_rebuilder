"""
strategies/__init__.py — Coinbase Bot Strategy Registry
"""
from .ma_crossover import MACrossoverStrategy
from .rsi_mean_reversion import RSIMeanReversionStrategy

STRATEGY_MAP = {
    "ma_crossover": MACrossoverStrategy,
    "rsi_mean_reversion": RSIMeanReversionStrategy,
}

__all__ = ["STRATEGY_MAP", "MACrossoverStrategy", "RSIMeanReversionStrategy"]
