import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import het_arch


#  Augmented Dickey-Fuller (ADF) Test for Stationarity
# -----------------------------------
# Choose ONE stock (GARCH is univariate)
# -----------------------------------
stock = "INFY.NS"   # change if you want

# -----------------------------------
# Extract log-return series
# -----------------------------------
series = returns_df.loc[
    returns_df["Ticker"] == stock, "log_return"
].values

# -----------------------------------
# Apply ADF test
# -----------------------------------
adf_result = adfuller(series, autolag="AIC")

# -----------------------------------
# Display results
# -----------------------------------
print(f"ADF Test Results for {stock}")
print(f"ADF Statistic : {adf_result[0]}")
print(f"p-value       : {adf_result[1]}")
print("Critical Values:")
for key, value in adf_result[4].items():
    print(f"   {key} : {value}")


# -----------------------------------
# Apply ARCH (Engle's ARCH LM Test)
# -----------------------------------
arch_test = het_arch(series, nlags=5)

# -----------------------------------
# Display results
# -----------------------------------
print(f"ARCH LM Test Results for {stock}")
print(f"LM Statistic  : {arch_test[0]}")
print(f"LM p-value    : {arch_test[1]}")
print(f"F Statistic   : {arch_test[2]}")
print(f"F p-value     : {arch_test[3]}")

