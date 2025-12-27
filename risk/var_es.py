import numpy as np
import pandas as pd
from scipy.stats import norm

# -------------------------------------------------
# VALUE AT RISK (VaR) & EXPECTED SHORTFALL (ES)
# SINGLE ASSET — GARCH BASED
# -------------------------------------------------

def compute_var_es(
    returns_df,
    garch_result,
    stock="INFY.NS",
    confidence_level=0.95
):
    """
    Computes Historical, Parametric and GARCH-based
    VaR & ES.
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
    # VALUE AT RISK (VaR)
    # -----------------------------------

    # 1️⃣ Historical VaR
    historical_var = np.quantile(returns, alpha)

    # 2️⃣ Parametric (Normal) VaR
    parametric_var = mu + sigma * z_score

    # 3️⃣ GARCH-based VaR
    garch_vol = garch_result.conditional_volatility
    garch_vol = garch_vol[-len(returns):]

    garch_var = mu + garch_vol * z_score

    var_df = pd.DataFrame({
        "Return": returns,
        "Historical_VaR": historical_var,
        "Parametric_VaR": parametric_var,
        "GARCH_VaR": garch_var
    })

    # VaR Backtesting
    var_df["Violation"] = var_df["Return"] < var_df["GARCH_VaR"]
    violation_rate = var_df["Violation"].mean()

    var_summary = pd.DataFrame({
        "Method": ["Historical", "Parametric", "GARCH"],
        "VaR (95%)": [
            historical_var,
            parametric_var,
            var_df["GARCH_VaR"].mean()
        ]
    })

    # -----------------------------------
    # EXPECTED SHORTFALL (ES)
    # -----------------------------------

    # 1️⃣ Historical ES
    historical_es = returns[
        returns <= historical_var
    ].mean()

    # 2️⃣ Parametric ES
    parametric_es = mu - sigma * (
        norm.pdf(z_score) / alpha
    )

    # 3️⃣ GARCH-based ES (NO look-ahead)
    garch_vol_series = pd.Series(garch_vol).shift(1)

    garch_es = mu - garch_vol_series * (
        norm.pdf(z_score) / alpha
    )

    es_df = pd.DataFrame({
        "Return": returns,
        "Historical_ES": historical_es,
        "Parametric_ES": parametric_es,
        "GARCH_ES": garch_es
    }).dropna()

    # ES Backtesting
    es_df["ES_Breach"] = es_df["Return"] < es_df["GARCH_ES"]
    es_breach_rate = es_df["ES_Breach"].mean()

    es_summary = pd.DataFrame({
        "Method": ["Historical", "Parametric", "GARCH"],
        "Expected Shortfall (95%)": [
            historical_es,
            parametric_es,
            es_df["GARCH_ES"].mean()
        ]
    })

    return {
        "VaR_Table": var_df,
        "VaR_Summary": var_summary,
        "VaR_Violation_Rate": violation_rate,
        "ES_Table": es_df,
        "ES_Summary": es_summary,
        "ES_Breach_Rate": es_breach_rate
    }

