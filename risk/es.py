import numpy as np
import pandas as pd
from scipy.stats import norm

# -------------------------------------------------
# EXPECTED SHORTFALL (ES / CVaR)
# SINGLE ASSET — GARCH BASED
# -------------------------------------------------

def compute_es(
    returns_df,
    garch_result,
    stock="INFY.NS",
    confidence_level=0.95
):
    """
    Computes Historical, Parametric and GARCH-based ES.
    Logic EXACTLY SAME as your Code 13.
    """

    # -----------------------------------
    # Prepare returns
    # -----------------------------------
    returns = returns_df.loc[
        returns_df["Ticker"] == stock,
        "log_return"
    ].values

    alpha = 1 - confidence_level
    z_score = norm.ppf(alpha)

    mu = np.mean(returns)
    sigma = np.std(returns)

    # -----------------------------------
    # 1️⃣ Historical ES
    # -----------------------------------
    historical_var = np.quantile(returns, alpha)

    historical_es = returns[
        returns <= historical_var
    ].mean()

    # -----------------------------------
    # 2️⃣ Parametric ES
    # -----------------------------------
    parametric_es = mu - sigma * (
        norm.pdf(z_score) / alpha
    )

    # -----------------------------------
    # 3️⃣ GARCH-based ES (NO look-ahead)
    # -----------------------------------
    garch_vol = pd.Series(
        garch_result.conditional_volatility
    ).shift(1)

    garch_vol = garch_vol[-len(returns):]

    garch_es = mu - garch_vol * (
        norm.pdf(z_score) / alpha
    )

    es_df = pd.DataFrame({
        "Return": returns,
        "Historical_ES": historical_es,
        "Parametric_ES": parametric_es,
        "GARCH_ES": garch_es
    }).dropna()

    # -----------------------------------
    # ES Backtesting
    # -----------------------------------
    es_df["ES_Breach"] = es_df["Return"] < es_df["GARCH_ES"]
    breach_rate = es_df["ES_Breach"].mean()

    # -----------------------------------
    # Summary
    # -----------------------------------
    es_summary = pd.DataFrame({
        "Method": ["Historical", "Parametric", "GARCH"],
        "Expected Shortfall (95%)": [
            historical_es,
            parametric_es,
            es_df["GARCH_ES"].mean()
        ]
    })

    return {
        "ES_Table": es_df,
        "ES_Summary": es_summary,
        "ES_Breach_Rate": breach_rate
    }
