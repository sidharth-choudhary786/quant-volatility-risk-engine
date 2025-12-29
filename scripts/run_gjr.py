import pandas as pd
from models.gjr_garch import fit_gjr_garch, extract_gjr_params

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
# Fit GJR-GARCH(1,1)
# -----------------------------------
gjr_result = fit_gjr_garch(series)

print(gjr_result.summary())

# -----------------------------------
# Extract parameters
# -----------------------------------
gjr_summary = extract_gjr_params(gjr_result)
gjr_summary["Ticker"] = stock

print("\nGJR-GARCH Parameters\n")
print(gjr_summary)
