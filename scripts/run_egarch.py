import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

import pandas as pd
from models.egarch import fit_egarch, extract_egarch_params

# -------------------------------
# Load clean returns dataset
# -------------------------------
returns_df = pd.read_csv(
    "data/processed/nifty50_log_returns_clean.csv"
)

# -------------------------------
# Choose ONE stock
# -------------------------------
stock = "INFY.NS"

series = returns_df.loc[
    returns_df["Ticker"] == stock,
    "log_return"
].values

# -------------------------------
# Fit EGARCH
# -------------------------------
egarch_result = fit_egarch(series)

# -------------------------------
# Print summary
# -------------------------------
print(egarch_result.summary())

# -------------------------------
# Extract parameters
# -------------------------------
egarch_summary = extract_egarch_params(egarch_result)
egarch_summary["Ticker"] = stock

print("\nEGARCH Parameters:")
print(egarch_summary)
