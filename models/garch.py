import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from arch import arch_model
from statsmodels.stats.diagnostic import het_arch


# GARCH is univariate , so Always model one stock at a time
# model fit on log return series of any stock

# -------------------------------
# Fit GARCH(1,1)
# -------------------------------
garch_model = arch_model(
    series,
    mean="Constant",     # mean = μ
    vol="GARCH",         # GARCH model
    p=1,                 # ARCH(1)
    q=1,                 # GARCH(1)
    dist="normal",       # Gaussian errors,
    rescale=False
)

garch_result = garch_model.fit(disp="off")

# -------------------------------
# Show results
# -------------------------------
print(garch_result.summary())


# Diagnostic checks for GARCH residuals


# -----------------------------------
# Extract standardized residuals
# -----------------------------------
std_resid = garch_result.std_resid

# -----------------------------------
# ARCH test on standardized residuals
# -----------------------------------
arch_test_resid = het_arch(std_resid, nlags=5)

print("ARCH LM Test on GARCH Residuals")
print(f"LM Statistic : {arch_test_resid[0]}")
print(f"LM p-value   : {arch_test_resid[1]}")


# Plot Conditional Volatility vs Squared Returns

# -----------------------------------
# Extract conditional volatility
# -----------------------------------
cond_vol = garch_result.conditional_volatility

# -----------------------------------
# Extract squared returns
# -----------------------------------
returns = series
squared_returns = returns ** 2

# -----------------------------------
# Plot
# -----------------------------------
plt.figure(figsize=(12, 5))

plt.plot(cond_vol, label="GARCH Conditional Volatility", color="blue")
plt.plot(squared_returns, label="Squared Returns", color="red", alpha=0.5)

plt.title("GARCH Conditional Volatility vs Squared Returns (INFY)")
plt.xlabel("Time")
plt.ylabel("Volatility")
plt.legend()
plt.show()



#  Volatility Forecasting using GARCH(1,1)


# -----------------------------------
# Forecast horizon
# -----------------------------------
horizon = 5   # forecast next 5 trading days

# -----------------------------------
# Generate volatility forecasts
# -----------------------------------
forecast = garch_result.forecast(horizon=horizon)

# -----------------------------------
# Extract variance forecasts
# -----------------------------------
variance_forecast = forecast.variance.values[-1]

# -----------------------------------
# Convert variance to volatility
# -----------------------------------
volatility_forecast = np.sqrt(variance_forecast)

# -----------------------------------
# Create readable output
# -----------------------------------
forecast_df = pd.DataFrame({
    "Day": range(1, horizon + 1),
    "Forecasted_Volatility": volatility_forecast
})

forecast_df


# last in-sample conditional volatility
last_vol = garch_result.conditional_volatility[-1]
last_vol

# extract parameters
omega = garch_result.params["omega"]
alpha = garch_result.params["alpha[1]"]
beta  = garch_result.params["beta[1]"]

# long-run volatility
long_run_vol = np.sqrt(omega / (1 - alpha - beta))
long_run_vol


#  Here i done with one stock INFY.NS
#  Now for all stocks (i create a function that work for all stocks)


def analyze_one_stock(ticker, returns_df):
    """
    Run full GARCH(1,1) pipeline for ONE stock.
    Returns results as a dictionary.
    """

    # -------------------------------
    # 1. Extract log-return series
    # -------------------------------
    series = returns_df.loc[
        returns_df["Ticker"] == ticker, "log_return"
    ].values

    # -------------------------------
    # 2. ADF Test (Stationarity)
    # -------------------------------
    adf_result = adfuller(series, autolag="AIC")
    adf_pvalue = adf_result[1]

    # -------------------------------
    # 3. ARCH LM Test (Volatility clustering)
    # -------------------------------
    arch_test = het_arch(series, nlags=5)
    arch_pvalue = arch_test[1]

    # -------------------------------
    # 4. Fit GARCH(1,1)
    # -------------------------------
    garch_model = arch_model(
        series,
        mean="Constant",
        vol="GARCH",
        p=1,
        q=1,
        dist="normal",
        rescale=False
    )

    garch_result = garch_model.fit(disp="off")

    # -------------------------------
    # 5. Extract GARCH parameters
    # -------------------------------
    omega = garch_result.params["omega"]
    alpha = garch_result.params["alpha[1]"]
    beta  = garch_result.params["beta[1]"]

    # -------------------------------
    # 6. Persistence & Long-run volatility
    # -------------------------------
    persistence = alpha + beta
    long_run_vol = np.sqrt(omega / (1 - persistence))

    # -------------------------------
    # 7. Model selection metrics
    # -------------------------------
    aic = garch_result.aic
    bic = garch_result.bic

    # -------------------------------
    # 8. Collect results
    # -------------------------------
    result = {
        "Ticker": ticker,
        "ADF_pvalue": adf_pvalue,
        "ARCH_pvalue": arch_pvalue,
        "alpha": alpha,
        "beta": beta,
        "persistence": persistence,
        "long_run_vol": long_run_vol,
        "AIC": aic,
        "BIC": bic
    }

    return result


#  Confirmation for one stock
analyze_one_stock("INFY.NS", returns_df)


#  Now Work on 10 stocks

# -------------------------------
# STEP A: Define 10 representative stocks
# -------------------------------
pilot_stocks = [
    "HDFCBANK.NS", "ICICIBANK.NS",     # Banking
    "INFY.NS", "TCS.NS",               # IT
    "RELIANCE.NS", "ONGC.NS",           # Energy
    "MARUTI.NS", "TATAMOTORS.NS",       # Auto
    "HINDUNILVR.NS", "SUNPHARMA.NS"     # FMCG / Pharma
]

# -------------------------------
# STEP B: Run GARCH analysis for 10 stocks
# -------------------------------
pilot_results = []
failed_pilot = []

for ticker in pilot_stocks:
    try:
        result = analyze_one_stock(ticker, returns_df)
        pilot_results.append(result)
    except Exception as e:
        failed_pilot.append(ticker)
        print(f"Failed for {ticker}: {e}")

# -------------------------------
# STEP C: Convert to DataFrame
# -------------------------------
pilot_df = pd.DataFrame(pilot_results)

# -------------------------------
# STEP D: Save pilot output
# -------------------------------
pilot_df.to_csv("garch_results_10stocks.csv", index=False)

pilot_df, failed_pilot



# -------------------------------
#  Run GARCH analysis for ALL 50 stocks
# -------------------------------
all_results = []
failed_all = []

for ticker in tickers:   # tickers = your full 50-stock list
    try:
        result = analyze_one_stock(ticker, returns_df)
        all_results.append(result)
    except Exception as e:
        failed_all.append(ticker)
        print(f"Failed for {ticker}: {e}")

# -------------------------------
# STEP F: Convert to DataFrame
# -------------------------------
all_df = pd.DataFrame(all_results)

# -------------------------------
# STEP G: Save full output
# -------------------------------
all_df.to_csv("garch_results_50stocks.csv", index=False)

all_df, failed_all



# -------------------------------
# STEP E: Run GARCH analysis for ALL 50 stocks
# -------------------------------
all_results = []
failed_all = []

for ticker in tickers:   # tickers = your full 50-stock list
    try:
        result = analyze_one_stock(ticker, returns_df)
        all_results.append(result)
    except Exception as e:
        failed_all.append(ticker)
        print(f"Failed for {ticker}: {e}")

# -------------------------------
# STEP F: Convert to DataFrame
# -------------------------------
all_df = pd.DataFrame(all_results)

# -------------------------------
# STEP G: Save full output
# -------------------------------
all_df.to_csv("garch_results_50stocks.csv", index=False)

all_df, failed_all

