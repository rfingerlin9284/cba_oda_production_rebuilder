"""
strategies/rsi_mean_reversion.py — RSI Mean Reversion Strategy (OANDA)

Signal logic:
  BUY  — RSI crosses up through oversold threshold (e.g. RSI goes from <30 to >=30)
  SELL — RSI crosses down through overbought threshold (e.g. RSI goes from >70 to <=70)
  HOLD — RSI in neutral zone or no crossover
"""
import pandas as pd
from .base_strategy import BaseStrategy


class RSIMeanReversionStrategy(BaseStrategy):
    """RSI mean-reversion strategy."""

    @staticmethod
    def _compute_rsi(series: pd.Series, period: int) -> pd.Series:
        delta = series.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
        rs = avg_gain / avg_loss.replace(0, float("inf"))
        return 100 - (100 / (1 + rs))

    def generate_signal(self, df: pd.DataFrame) -> str:
        period = self.config.RSI_PERIOD
        oversold = self.config.RSI_OVERSOLD
        overbought = self.config.RSI_OVERBOUGHT

        if len(df) < period + 1:
            return "HOLD"

        rsi = self._compute_rsi(df["close"], period)
        prev_rsi = rsi.iloc[-2]
        curr_rsi = rsi.iloc[-1]

        if prev_rsi < oversold and curr_rsi >= oversold:
            return "BUY"
        if prev_rsi > overbought and curr_rsi <= overbought:
            return "SELL"
        return "HOLD"
