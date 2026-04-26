"""
strategies/ma_crossover.py — Moving-Average Crossover Strategy (Coinbase)
"""
import pandas as pd
from .base_strategy import BaseStrategy


class MACrossoverStrategy(BaseStrategy):
    """Dual EMA crossover strategy."""

    def generate_signal(self, df: pd.DataFrame) -> str:
        fast = self.config.MA_FAST
        slow = self.config.MA_SLOW

        if len(df) < slow + 1:
            return "HOLD"

        df = df.copy()
        df["ema_fast"] = df["close"].ewm(span=fast, adjust=False).mean()
        df["ema_slow"] = df["close"].ewm(span=slow, adjust=False).mean()

        prev_fast = df["ema_fast"].iloc[-2]
        prev_slow = df["ema_slow"].iloc[-2]
        curr_fast = df["ema_fast"].iloc[-1]
        curr_slow = df["ema_slow"].iloc[-1]

        if prev_fast <= prev_slow and curr_fast > curr_slow:
            return "BUY"
        if prev_fast >= prev_slow and curr_fast < curr_slow:
            return "SELL"
        return "HOLD"
