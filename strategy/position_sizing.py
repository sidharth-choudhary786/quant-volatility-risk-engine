import numpy as np
import pandas as pd


def volatility_target_position(
    forecasted_volatility,
    target_vol=0.01,
    min_pos=0.1,
    max_pos=2.0
):
    """
    Volatility targeting position sizing (YOUR ORIGINAL LOGIC)

    Formula:
        Position Size = target_vol / forecasted_volatility

    With risk caps:
        min_pos <= Position_Size <= max_pos

    Parameters
    ----------
    forecasted_volatility : pd.Series or np.ndarray
        Volatility estimate (e.g., GARCH conditional volatility)

    target_vol : float, default=0.01
        Target daily volatility (1% daily risk)

    min_pos : float, default=0.1
        Minimum exposure

    max_pos : float, default=2.0
        Maximum exposure (leverage cap)

    Returns
    -------
    pd.Series
        Position size series
    """

    position_size = target_vol / forecasted_volatility

    # Risk control (EXACT SAME as your .clip logic)
    position_size = np.clip(position_size, min_pos, max_pos)

    return pd.Series(position_size, index=forecasted_volatility.index, name="Position_Size")

