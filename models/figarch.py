import numpy as np
import pandas as pd
from arch import arch_model


# -----------------------------------
# STEP 1: Select one stock
# -----------------------------------
stock = "INFY.NS"

# -----------------------------------
# STEP 2: Extract log returns
# -----------------------------------
series = returns_df.loc[
    returns_df["Ticker"] == stock, "log_return"
].values

# -----------------------------------
# STEP 3: Fit FIGARCH(1,1)
# -----------------------------------
figarch_model = arch_model(
    series,
    mean="Constant",
    vol="FIGARCH",
    p=1,
    q=1,
    dist="normal",
    rescale=False
)

figarch_result = figarch_model.fit(disp="off")

# -----------------------------------
# STEP 4: Show summary
# -----------------------------------
print(figarch_result.summary())

# Extract long memory parameter
d_param = figarch_result.params["d"]

# Store result
figarch_summary = {
    "Ticker": stock,
    "d_parameter": d_param,
    "AIC": figarch_result.aic,
    "BIC": figarch_result.bic
}

figarch_summary


# pick first 10 stocks
stock_list_10 = returns_df["Ticker"].unique()[:10]

figarch_results_10 = []

for stock in stock_list_10:
    series = returns_df.loc[
        returns_df["Ticker"] == stock, "log_return"
    ].values

    try:
        model = arch_model(
            series,
            mean="Constant",
            vol="FIGARCH",
            p=1,
            q=1,
            dist="normal",
            rescale=False
        )

        result = model.fit(disp="off")

        figarch_results_10.append({
            "Ticker": stock,
            "d_parameter": result.params["d"],
            "AIC": result.aic,
            "BIC": result.bic
        })

    except Exception as e:
        figarch_results_10.append({
            "Ticker": stock,
            "d_parameter": np.nan,
            "AIC": np.nan,
            "BIC": np.nan
        })

figarch_10_df = pd.DataFrame(figarch_results_10)
figarch_10_df


# for 50 stocks
stock_list_50 = returns_df["Ticker"].unique()

figarch_results_50 = []

for stock in stock_list_50:
    series = returns_df.loc[
        returns_df["Ticker"] == stock, "log_return"
    ].values

    try:
        model = arch_model(
            series,
            mean="Constant",
            vol="FIGARCH",
            p=1,
            q=1,
            dist="normal",
            rescale=False
        )

        result = model.fit(disp="off")

        figarch_results_50.append({
            "Ticker": stock,
            "d_parameter": result.params["d"],
            "AIC": result.aic,
            "BIC": result.bic
        })

    except:
        figarch_results_50.append({
            "Ticker": stock,
            "d_parameter": np.nan,
            "AIC": np.nan,
            "BIC": np.nan
        })

figarch_50_df = pd.DataFrame(figarch_results_50)

figarch_50_df.to_csv("figarch_50stocks.csv", index=False)



# COMPARE GARCH & FIGARCH

# Load GARCH results
garch_50_df = pd.read_csv("garch_results_50stocks.csv")

# Load FIGARCH results
figarch_50_df = pd.read_csv("figarch_50stocks.csv")

comparison_df = pd.merge(
    garch_50_df,
    figarch_50_df,
    on="Ticker",
    suffixes=("_GARCH", "_FIGARCH")
)


comparison_df["Better_Model"] = np.where(
    comparison_df["AIC_GARCH"] < comparison_df["AIC_FIGARCH"],
    "GARCH",
    "FIGARCH"
)

comparison_df


