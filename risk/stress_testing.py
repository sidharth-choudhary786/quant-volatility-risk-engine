import numpy as np
import pandas as pd
from scipy.stats import norm

# -------------------------------------------------
# STRESS TESTING & SCENARIO ANALYSIS
# SINGLE ASSET — GARCH BASED
# -------------------------------------------------

def run_stress_testing(
    returns,
    garch_vol,
    confidence_level=0.99,
    stress_multiplier=3,
    horizon_days=5
):
    """
    Stress testing using:
    1. Worst historical loss
    2. GARCH volatility shock
    3. Multi-day crisis scenario

    Logic EXACTLY SAME as Code 14
    """

    # -----------------------------------
    # SAFETY: align lengths & remove NaN
    # -----------------------------------
    returns = np.asarray(returns)
    garch_vol = np.asarray(garch_vol)

    min_len = min(len(returns), len(garch_vol))
    returns = returns[-min_len:]
    garch_vol = garch_vol[-min_len:]

    returns = returns[np.isfinite(returns)]
    garch_vol = garch_vol[np.isfinite(garch_vol)]

    # -----------------------------------
    # 1️⃣ Worst historical day
    # -----------------------------------
    worst_daily_loss = abs(np.min(returns))

    # -----------------------------------
    # 2️⃣ GARCH volatility shock
    # -----------------------------------
    latest_vol = garch_vol[-1]
    z_score = norm.ppf(1 - confidence_level)

    garch_stress_loss = abs(
        z_score * latest_vol * stress_multiplier
    )

    # -----------------------------------
    # 3️⃣ Multi-day crisis scenario
    # -----------------------------------
    multi_day_stress_loss = abs(
        np.sqrt(horizon_days) * garch_stress_loss
    )

    # -----------------------------------
    # Summary table
    # -----------------------------------
    stress_summary = pd.DataFrame({
        "Scenario": [
            "Worst Historical Day",
            "GARCH Volatility Shock (1-Day)",
            f"GARCH Volatility Shock ({horizon_days}-Day)"
        ],
        "Estimated Loss": [
            worst_daily_loss,
            garch_stress_loss,
            multi_day_stress_loss
        ]
    })

    return stress_summary
