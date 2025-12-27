import numpy as np
import pandas as pd
from arch import arch_model

# GJR-GARCH on ONE stock (INFY)

# -----------------------------------
# STEP 1: Choose one stock
# -----------------------------------
stock = "INFY.NS"

# -----------------------------------
# STEP 2: Extract log returns
# -----------------------------------
series = returns_df.loc[
    returns_df["Ticker"] == stock, "log_return"
].values

# -----------------------------------
# STEP 3: Fit GJR-GARCH(1,1)
# -----------------------------------
gjr_model = arch_model(
    series,
    mean="Constant",
    vol="GARCH",
    p=1,
    o=1,     # <-- THIS enables GJR term
    q=1,
    dist="normal",
    rescale=False
)

gjr_result = gjr_model.fit(disp="off")

# -----------------------------------
# STEP 4: Show summary
# -----------------------------------
print(gjr_result.summary())


# Extract parameters
omega = gjr_result.params["omega"]
alpha = gjr_result.params["alpha[1]"]
beta  = gjr_result.params["beta[1]"]
gamma = gjr_result.params["gamma[1]"]

# Persistence (fear-adjusted)
persistence = alpha + beta + 0.5 * gamma

# Store results
gjr_summary = {
    "Ticker": stock,
    "omega": omega,
    "alpha": alpha,
    "beta": beta,
    "gamma": gamma,
    "persistence": persistence,
    "AIC": gjr_result.aic,
    "BIC": gjr_result.bic
}

gjr_summary


# COMPARISON of ALL MODELS ( GARCH, EGARCH, GJR-GARCH)
model_compare = pd.DataFrame({
    "Model": ["GARCH", "EGARCH", "GJR-GARCH"],
    "AIC": [
        garch_result.aic,
        egarch_result.aic,
        gjr_result.aic
    ],
    "BIC": [
        garch_result.bic,
        egarch_result.bic,
        gjr_result.bic
    ]
})

model_compare


# Scale for 10 & 50 stocks

def analyze_gjr_one_stock(ticker, returns_df):
    """
    Fit GJR-GARCH(1,1) for one stock and return key parameters
    """

    # -------------------------------
    # 1. Extract log returns
    # -------------------------------
    series = returns_df.loc[
        returns_df["Ticker"] == ticker, "log_return"
    ].values

    # -------------------------------
    # 2. Fit GJR-GARCH(1,1)
    # -------------------------------
    gjr_model = arch_model(
        series,
        mean="Constant",
        vol="GARCH",
        p=1,
        o=1,   # asymmetry (fear) term
        q=1,
        dist="normal",
        rescale=False
    )

    gjr_result = gjr_model.fit(disp="off")

    # -------------------------------
    # 3. Extract parameters
    # -------------------------------
    omega = gjr_result.params["omega"]
    alpha = gjr_result.params["alpha[1]"]
    beta  = gjr_result.params["beta[1]"]
    gamma = gjr_result.params["gamma[1]"]

    # -------------------------------
    # 4. Persistence (fear-adjusted)
    # -------------------------------
    persistence = alpha + beta + 0.5 * gamma

    return {
        "Ticker": ticker,
        "omega": omega,
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "persistence": persistence,
        "AIC": gjr_result.aic,
        "BIC": gjr_result.bic
    }

# for 10 stocks
pilot_stocks = [
    "HDFCBANK.NS", "ICICIBANK.NS",
    "INFY.NS", "TCS.NS",
    "RELIANCE.NS", "ONGC.NS",
    "MARUTI.NS", "TATAMOTORS.NS",
    "HINDUNILVR.NS", "SUNPHARMA.NS"
]

gjr_pilot_results = []
gjr_failed_pilot = []

for ticker in pilot_stocks:
    try:
        result = analyze_gjr_one_stock(ticker, returns_df)
        gjr_pilot_results.append(result)
    except Exception as e:
        gjr_failed_pilot.append(ticker)
        print(f"GJR failed for {ticker}: {e}")

gjr_pilot_df = pd.DataFrame(gjr_pilot_results)

gjr_pilot_df, gjr_failed_pilot


# for 50 stocks
gjr_results = []
gjr_failed = []

for ticker in tickers:   # full NIFTY-50 list
    try:
        result = analyze_gjr_one_stock(ticker, returns_df)
        gjr_results.append(result)
    except Exception as e:
        gjr_failed.append(ticker)
        print(f"GJR failed for {ticker}: {e}")

gjr_df = pd.DataFrame(gjr_results)

# Save output
gjr_df.to_csv("gjr_garch_50stocks.csv", index=False)

gjr_df, gjr_failed


# Sort by gamma (highest fear first)
fear_rank = gjr_df.sort_values("gamma", ascending=False)

top_fear_stocks = fear_rank.head(10)
low_fear_stocks = fear_rank.tail(10)

top_fear_stocks, low_fear_stocks



# ------------------------------------------------
# FUNCTION: Compare GARCH vs EGARCH vs GJR for ONE stock then for all stocks
# ------------------------------------------------
def compare_models_one_stock(ticker, returns_df):
    """
    Fit GARCH, EGARCH, and GJR-GARCH for one stock
    and return AIC/BIC comparison.
    """

    # -------------------------------
    # 1. Extract log returns
    # -------------------------------
    series = returns_df.loc[
        returns_df["Ticker"] == ticker, "log_return"
    ].values

    # for removing data scaling warnings
    # series = series * 100
    # -------------------------------
    # 2. Fit GARCH(1,1)
    # -------------------------------
    garch = arch_model(
        series,
        mean="Constant",
        vol="GARCH",
        p=1, q=1,
        dist="normal",
        # for hiding data scaling warnings
        rescale=False
    ).fit(disp="off")

    # -------------------------------
    # 3. Fit EGARCH(1,1)
    # -------------------------------
    egarch = arch_model(
        series,
        mean="Constant",
        vol="EGARCH",
        p=1, q=1,
        dist="normal",
        rescale=False
    ).fit(disp="off")

    # -------------------------------
    # 4. Fit GJR-GARCH(1,1)
    # -------------------------------
    gjr = arch_model(
        series,
        mean="Constant",
        vol="GARCH",
        p=1, o=1, q=1,
        dist="normal",
        rescale=False
    ).fit(disp="off")

    # -------------------------------
    # 5. Collect AIC/BIC
    # -------------------------------
    results = {
        "Ticker": ticker,

        "AIC_GARCH": garch.aic,
        "AIC_EGARCH": egarch.aic,
        "AIC_GJR": gjr.aic,

        "BIC_GARCH": garch.bic,
        "BIC_EGARCH": egarch.bic,
        "BIC_GJR": gjr.bic
    }

    # -------------------------------
    # 6. Select best model (lowest AIC)
    # -------------------------------
    aic_values = {
        "GARCH": garch.aic,
        "EGARCH": egarch.aic,
        "GJR-GARCH": gjr.aic
    }

    best_model = min(aic_values, key=aic_values.get)
    results["Best_Model"] = best_model

    return results


# ------------------------------------------------
# RUN COMPARISON FOR ALL STOCKS
# ------------------------------------------------
comparison_results = []
failed_stocks = []

for ticker in tickers:
    try:
        res = compare_models_one_stock(ticker, returns_df)
        comparison_results.append(res)
    except Exception as e:
        failed_stocks.append(ticker)
        print(f"Failed for {ticker}: {e}")

# ------------------------------------------------
# FINAL RESULT TABLE
# ------------------------------------------------
comparison_df = pd.DataFrame(comparison_results)

# Save output
comparison_df.to_csv("model_comparison_50stocks.csv", index=False)

comparison_df, failed_stocks

