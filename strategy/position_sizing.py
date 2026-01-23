import numpy as np
import pandas as pd

def volatility_target_position(
    forecasted_volatility,
    target_vol=0.01,
    min_pos=0.0,
    max_pos=1.0
):
    """
    Volatility targeting position sizing (REALISTIC, NO LEVERAGE)

    Formula:
        Position Size = target_vol / forecasted_volatility

    Constraints:
        0 <= Position_Size <= 1.0  (NO leverage)

    This ensures:
    - No hidden leverage
    - Institutional realism
    - Clean risk interpretation
    """

    position_size = target_vol / forecasted_volatility

    # HARD leverage cap (CRITICAL FIX)
    position_size = np.clip(position_size, min_pos, max_pos)

    return pd.Series(
        position_size,
        index=forecasted_volatility.index,
        name="Position_Size"
    )
