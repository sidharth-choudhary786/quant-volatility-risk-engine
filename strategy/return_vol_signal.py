import numpy as np
import pandas as pd

def compute_return_vol_signal(df, lookback=20):
    """
    Risk-adjusted expected return signal:
    Expected Return / Forecasted Volatility
    """

    # Rolling expected return
    df["Exp_Return"] = (
        df["log_return"]
        .rolling(lookback)
        .mean()
    )

    # Risk-adjusted signal
    df["RV_Signal"] = (
        df["Exp_Return"]
        / df["Forecasted_Volatility"]
    )

    # Safety clipping
    df["RV_Signal"] = df["RV_Signal"].clip(-3, 3)

    return df

