"""
strategies/base_strategy.py — Abstract base for all OANDA strategies
"""
from abc import ABC, abstractmethod
import pandas as pd


class BaseStrategy(ABC):
    """All OANDA strategies must inherit this class."""

    def __init__(self, config) -> None:
        self.config = config

    @abstractmethod
    def generate_signal(self, df: pd.DataFrame) -> str:
        """
        Analyse a candle DataFrame and return a signal string.

        Parameters
        ----------
        df : pd.DataFrame
            OHLCV DataFrame with columns: open, high, low, close, volume.
            Index is a DatetimeIndex.  Sorted oldest → newest.

        Returns
        -------
        str
            One of: "BUY" | "SELL" | "HOLD"
        """
        ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
