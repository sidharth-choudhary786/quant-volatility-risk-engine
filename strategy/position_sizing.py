import numpy as np
import pandas as pd

def volatility_target_position(
    forecasted_volatility: pd.Series,
    target_vol: float = 0.01,
    min_pos: float = 0.0,
    max_pos: float = 1.0
):
    """
    Volatility targeting position sizing (NO LEVERAGE, REALISTIC)

    Formula:
        Position_Size = target_vol / forecasted_volatility

    Constraints:
        min_pos <= Position_Size <= max_pos

    This guarantees:
    - No hidden leverage
    - Institutional realism
    - Stable risk interpretation
    """

    print("🔥 USING FIXED POSITION SIZING FUNCTION 🔥")

    position_size = target_vol / forecasted_volatility

    # HARD leverage cap (FINAL SAFETY)
    position_size = np.clip(position_size, min_pos, max_pos)

    return pd.Series(
        position_size,
        index=forecasted_volatility.index,
        name="Position_Size"
    )
