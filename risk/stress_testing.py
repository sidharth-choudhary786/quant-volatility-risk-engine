import numpy as np
import pandas as pd
from scipy.stats import norm

# -------------------------------------------------
# STRESS TESTING & SCENARIO ANALYSIS
# -------------------------------------------------

def run_stress_tests(
    returns_df,
    garch_result,
    stock="INFY.NS",
    stress_multiplier=3
):
    """
    Stress testing based on:
    1. Worst historical day
    2. GARCH volatility shock
    3. Multi-day crisis scenario

    Logic EXACTLY SAME as Code 14.
    """

    # -----------------------------------
    # Prepare returns
    # -----------------------------------
    returns = returns_df.loc[
        returns_df["Ticker"] == stock,
        "log_return"
    ].values

    # -----------------------------------
    # 1️⃣ HISTORICAL STRESS TEST
    # -----------------------------------
    worst_daily_loss = abs(returns.min())

    # -----------------------------------
    # 2️⃣ GARCH VOLATILITY SHOCK
    # -----------------------------------
    garch_vol = pd.Series(garch_result.conditional_volatility)
    latest_vol = garch_vol.iloc[-1]

    z_99 = norm.ppf(0.01)

    garch_stress_loss = abs(
        z_99 * latest_vol * stress_multiplier
    )

    # -----------------------------------
    # 3️⃣ MULTI-DAY CRISIS (5-Day)
    # -----------------------------------
    days = 5
    multi_day_stress_loss = abs(
        np.sqrt(days) * garch_stress_loss
    )

    # -----------------------------------
    # Summary Table
    # -----------------------------------
    stress_summary = pd.DataFrame({
        "Scenario": [
            "Worst Historical Day",
            "GARCH Volatility Shock (1-Day)",
            "GARCH Volatility Shock (5-Day)"
        ],
        "Estimated Loss": [
            worst_daily_loss,
            garch_stress_loss,
            multi_day_stress_loss
        ]
    })

    return {
        "Worst_Daily_Loss": worst_daily_loss,
        "GARCH_Stress_1D": garch_stress_loss,
        "GARCH_Stress_5D": multi_day_stress_loss,
        "Stress_Summary": stress_summary
    }

