import pandas as pd
from models.figarch import fit_figarch, extract_figarch_params

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
# Fit FIGARCH(1,1)
# -----------------------------------
figarch_result = fit_figarch(series)

print(figarch_result.summary())

# -----------------------------------
# Extract parameters
# -----------------------------------
figarch_summary = extract_figarch_params(figarch_result)
figarch_summary["Ticker"] = stock

print("\nFIGARCH Parameters\n")
print(figarch_summary)
