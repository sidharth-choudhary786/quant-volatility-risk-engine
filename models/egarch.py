import numpy as np
import pandas as pd
from arch import arch_model


#  EGARCH (Exponential GARCH)

# -----------------------------------
# STEP 1: Load clean returns dataset
# -----------------------------------
returns_df = pd.read_csv(
    "nifty50_history_with_adj/nifty50_log_returns_clean.csv"
)

# -----------------------------------
# STEP 2: Choose ONE stock first
# (EGARCH must be tested on one stock before scaling)
# -----------------------------------
stock = "INFY.NS"

# -----------------------------------
# STEP 3: Extract log-return series
# -----------------------------------
series = returns_df.loc[
    returns_df["Ticker"] == stock, "log_return"
].values

# -----------------------------------
# STEP 4: Fit EGARCH(1,1)
# -----------------------------------
egarch_model = arch_model(
    series,
    mean="Constant",
    vol="EGARCH",
    p=1,
    o=1,
    q=1,
    dist="normal",
    rescale=False
)

egarch_result = egarch_model.fit(disp="off")

# -----------------------------------
# STEP 5: Show EGARCH results
# -----------------------------------
print(egarch_result.summary())

# -----------------------------------
# STEP 6: Extract EGARCH parameters
# -----------------------------------
omega = egarch_result.params["omega"]
alpha = egarch_result.params["alpha[1]"]
beta  = egarch_result.params["beta[1]"]
gamma = egarch_result.params["gamma[1]"]

# -----------------------------------
# STEP 7: Save key results
# -----------------------------------
egarch_summary = {
    "Ticker": stock,
    "omega": omega,
    "alpha": alpha,
    "beta": beta,
    "gamma": gamma,
    "persistence": alpha + beta,
    "AIC": egarch_result.aic,
    "BIC": egarch_result.bic
}

egarch_summary



# EGARCH for one Stock (INFY.NS)

def analyze_egarch_one_stock(ticker, returns_df):
    """
    Run EGARCH(1,1) for one stock and return key results.
    """

    # -------------------------------
    # 1. Extract log returns
    # -------------------------------
    series = returns_df.loc[
        returns_df["Ticker"] == ticker, "log_return"
    ].values

    # -------------------------------
    # 2. Fit EGARCH(1,1)
    # -------------------------------
    egarch_model = arch_model(
        series,
        mean="Constant",
        vol="EGARCH",
        p=1,
        o=1,
        q=1,
        dist="normal",
        rescale=False
    )

    egarch_result = egarch_model.fit(disp="off")

    # -------------------------------
    # 3. Extract parameters
    # -------------------------------
    omega = egarch_result.params["omega"]
    alpha = egarch_result.params["alpha[1]"]
    beta  = egarch_result.params["beta[1]"]
    gamma = egarch_result.params["gamma[1]"]
    # # robust gamma extraction (works for all stocks & arch versions)
    # gamma_keys = [k for k in egarch_result.params.index if k.startswith("gamma")]

    # if len(gamma_keys) == 0:
    #     raise ValueError("Gamma parameter not found in EGARCH model")

    # gamma = egarch_result.params[gamma_keys[0]]


    # -------------------------------
    # 4. Store results
    # -------------------------------
    result = {
        "Ticker": ticker,
        "omega": omega,
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "persistence": alpha + beta,
        "AIC": egarch_result.aic,
        "BIC": egarch_result.bic
    }

    return result


# EGARCH for 10 Stocks
# Pick same 10 representative stocks
pilot_stocks = [
    "HDFCBANK.NS", "ICICIBANK.NS",
    "INFY.NS", "TCS.NS",
    "RELIANCE.NS", "ONGC.NS",
    "MARUTI.NS", "TATAMOTORS.NS",
    "HINDUNILVR.NS", "SUNPHARMA.NS"
]

pilot_results = []
failed_pilot = []

for ticker in pilot_stocks:
    try:
        result = analyze_egarch_one_stock(ticker, returns_df)
        pilot_results.append(result)
    except Exception as e:
        failed_pilot.append(ticker)
        print(f"Failed for {ticker}: {e}")

pilot_df = pd.DataFrame(pilot_results)
pilot_df, failed_pilot


#  EGARCH for ALL 50 STOCKS
egarch_results = []
failed_egarch = []

for ticker in tickers:   # tickers = full NIFTY-50 list
    try:
        result = analyze_egarch_one_stock(ticker, returns_df)
        egarch_results.append(result)
    except Exception as e:
        failed_egarch.append(ticker)
        print(f"Failed for {ticker}: {e}")

egarch_df = pd.DataFrame(egarch_results)

# Save results
egarch_df.to_csv("egarch_50stocks.csv", index=False)

egarch_df, failed_egarch


# Sort stocks by gamma (most negative first)
fear_ranking = egarch_df.sort_values("gamma").reset_index(drop=True)

# Top fear-driven stocks
top_fear_stocks = fear_ranking.head(10)

# Least fear-driven stocks
low_fear_stocks = fear_ranking.tail(10)

top_fear_stocks, low_fear_stocks

