import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# I WORK ON ADJ CLOSE ONLY , NO NEED FOR CLOSE
#  ---- Load combined CSV ----
df = pd.read_csv("nifty50_history_with_adj/nifty50_combined_2015_2025.csv", parse_dates=["Date"])

# ---- Sort by Ticker + Date ----
df = df.sort_values(["Ticker", "Date"]).reset_index(drop=True)

# ---- Ensure Adj Close exists ----
if "Adj Close" not in df.columns:
    raise ValueError("Adj Close column missing in combined CSV!")

# ---- Compute log returns using Adj Close only ----
df["log_return"] = df.groupby("Ticker")["Adj Close"].transform(
    lambda x: np.log(x / x.shift(1))
)


# ---- Save final output ----
output_path = "nifty50_history_with_adj/nifty50_log_returns_adjclose.csv"
df.to_csv(output_path, index=False)

print("Daily log-return file created (Adj Close only):")
print(output_path)

# drop the first row of each stock , because log returns missing(we shift one row) at first date on each stock
df = df.dropna(subset=["log_return"])
# reset index , index wil be 1 2 3 ... (not 0 1 2 3 ...)
df = df.reset_index(drop=True)
df.index = df.index + 1
# remove timezone 00:00:00 + 5:30 , because our data is daily basis , so no need for this type time zone
df["Date"] = pd.to_datetime(df["Date"]).dt.date

# keep only essential columns
returns_df = df[["Date", "Ticker", "Adj Close", "Volume", "log_return"]]

# save clean returns dataset
returns_df.to_csv(
    "nifty50_history_with_adj/nifty50_log_returns_clean.csv",
    index=False
)
rows_per_stock = df.groupby("Ticker").size().reset_index(name="row_count")
rows_per_stock
# SHREE CEMENT did not have data for one trading day in the 2015–2025 window compared to others
# all stocks have 2694 total data but SHREECEM.NS have only 2693 (one day data is missed). total rows are 134699 instead 134700
returns_df

# RETURN & VOLATILITY PLOTS (Sanity Check for GARCH)
# Choose ONE stock for inspection
# (GARCH is always checked stock-wise)
stock = "INFY.NS"

# -------------------------------
# Filter data for that stock
# -------------------------------
stock_df = returns_df[returns_df["Ticker"] == stock].copy()

# -------------------------------
# Plot 1: Daily Log Returns
# -------------------------------
plt.figure(figsize=(12, 4))
plt.plot(stock_df["Date"], stock_df["log_return"])
plt.title(f"Daily Log Returns - {stock}")
plt.xlabel("Date")
plt.ylabel("Log Return")
plt.show()

# -------------------------------
# Plot 2: Squared Log Returns
# (proxy for volatility clustering)
# -------------------------------
plt.figure(figsize=(12, 4))
plt.plot(stock_df["Date"], stock_df["log_return"]**2)
plt.title(f"Squared Log Returns (Volatility Proxy) - {stock}")
plt.xlabel("Date")
plt.ylabel("Squared Log Return")
plt.show()
