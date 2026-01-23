import pandas as pd

def detect_volatility_regime(vol_series, window=60):
    """
    Detect LOW / MEDIUM / HIGH volatility regimes
    using rolling quantiles (NO look-ahead).
    """

    vol = pd.Series(vol_series).reset_index(drop=True)

    low_q  = vol.rolling(window).quantile(0.33)
    high_q = vol.rolling(window).quantile(0.66)

    regimes = []

    for v, l, h in zip(vol, low_q, high_q):
        if pd.isna(l) or pd.isna(h):
            regimes.append("MEDIUM")  # FIX: no UNKNOWN
        elif v < l:
            regimes.append("LOW")
        elif v < h:
            regimes.append("MEDIUM")
        else:
            regimes.append("HIGH")

    return pd.Series(regimes, index=vol.index, name="Vol_Regime")
