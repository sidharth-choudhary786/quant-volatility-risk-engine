import numpy as np
import pandas as pd
from scipy.stats import norm

# -------------------------------------------------
# VALUE AT RISK (VaR)
# SINGLE ASSET — GARCH BASED
# -------------------------------------------------

__all__ = ["compute_var"]


def compute_var(
    returns_df,
    garch_result,
    stock="INFY.NS",
    confidence_level=0.95
):
    """
    Computes Historical, Parametric and GARCH-based VaR.
    Logic EXACTLY SAME as your Code 13.
    """

    # -----------------------------------
    # Prepare returns (NO NaN, NO mismatch)
    # -----------------------------------
    returns = returns_df.loc[
        returns_df["Ticker"] == stock,
        "log_return"
    ].dropna().values

    garch_vol = np.asarray(
        garch_result.conditional_volatility
    )

    # -----------------------------------
    # ALIGN LENGTHS (CRITICAL FIX)
    # -----------------------------------
    min_len = min(len(returns), len(garch_vol))
    returns = returns[-min_len:]
    garch_vol = garch_vol[-min_len:]

    alpha = 1 - confidence_level
    z_score = norm.ppf(alpha)

    mu = np.mean(returns)
    sigma = np.std(returns)

    # -----------------------------------
    # 1️⃣ Historical VaR
    # -----------------------------------
    historical_var = np.quantile(returns, alpha)

    # -----------------------------------
    # 2️⃣ Parametric (Normal) VaR
    # -----------------------------------
    parametric_var = mu + sigma * z_score

    # -----------------------------------
    # 3️⃣ GARCH-based VaR
    # -----------------------------------
    garch_var = mu + garch_vol * z_score

    # -----------------------------------
    # VaR Table
    # -----------------------------------
    var_df = pd.DataFrame({
        "Return": returns,
        "Historical_VaR": historical_var,
        "Parametric_VaR": parametric_var,
        "GARCH_VaR": garch_var
    })

    # -----------------------------------
    # VaR Backtesting
    # -----------------------------------
    var_df["Violation"] = var_df["Return"] < var_df["GARCH_VaR"]
    violation_rate = var_df["Violation"].mean()

    # -----------------------------------
    # Summary
    # -----------------------------------
    var_summary = pd.DataFrame({
        "Method": ["Historical", "Parametric", "GARCH"],
        "VaR (95%)": [
            historical_var,
            parametric_var,
            var_df["GARCH_VaR"].mean()
        ]
    })

    return {
        "VaR_Table": var_df,
        "VaR_Summary": var_summary,
        "VaR_Violation_Rate": violation_rate
    }
