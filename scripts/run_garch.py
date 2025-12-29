import pandas as pd
from models.garch import fit_garch, extract_garch_params

# -----------------------------------
# Load clean returns data
# -----------------------------------
returns_df = pd.read_csv(
    "nifty50_history_with_adj/nifty50_log_returns_clean.csv"
)

# -----------------------------------
# Choose pilot stock
# -----------------------------------
stock = "INFY.NS"

series = returns_df.loc[
    returns_df["Ticker"] == stock,
    "log_return"
].values

# -----------------------------------
# Fit GARCH(1,1)
# -----------------------------------
garch_result = fit_garch(series)

print(garch_result.summary())

# -----------------------------------
# Extract parameters
# -----------------------------------
garch_summary = extract_garch_params(garch_result)
garch_summary["Ticker"] = stock

print("\nGARCH Parameters\n")
print(garch_summary)
