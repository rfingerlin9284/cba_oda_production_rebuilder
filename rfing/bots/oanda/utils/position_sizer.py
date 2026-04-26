"""
utils/position_sizer.py — Risk-based position sizing for OANDA
"""
from __future__ import annotations


def compute_units(
    balance: float,
    risk_fraction: float,
    stop_pips: float,
    pip_value_per_unit: float = 0.0001,
) -> int:
    """
    Compute the number of units to trade based on fixed fractional risk.

    Parameters
    ----------
    balance           : Account balance in account currency (e.g. USD).
    risk_fraction     : Fraction of balance to risk per trade (e.g. 0.01 = 1 %).
    stop_pips         : Distance from entry to stop-loss in pips.
    pip_value_per_unit: Value of 1 pip for 1 unit of the instrument.
                        For most USD-denominated pairs this is 0.0001.

    Returns
    -------
    int : Number of units (always positive; caller determines direction).
    """
    if stop_pips <= 0 or pip_value_per_unit <= 0:
        return 0
    risk_amount = balance * risk_fraction
    units = risk_amount / (stop_pips * pip_value_per_unit)
    return max(1, int(units))
