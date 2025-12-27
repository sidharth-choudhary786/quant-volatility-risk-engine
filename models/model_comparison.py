import pandas as pd

garch_df   = pd.read_csv("garch_results_50stocks.csv")
egarch_df  = pd.read_csv("egarch_50stocks.csv")
gjr_df     = pd.read_csv("gjr_garch_50stocks.csv")
figarch_df = pd.read_csv("figarch_50stocks.csv")

garch_df   = garch_df[["Ticker","AIC","BIC"]].rename(
    columns={"AIC":"AIC_GARCH","BIC":"BIC_GARCH"}
)
egarch_df  = egarch_df[["Ticker","AIC","BIC"]].rename(
    columns={"AIC":"AIC_EGARCH","BIC":"BIC_EGARCH"}
)
gjr_df     = gjr_df[["Ticker","AIC","BIC"]].rename(
    columns={"AIC":"AIC_GJR","BIC":"BIC_GJR"}
)
figarch_df = figarch_df[["Ticker","AIC","BIC"]].rename(
    columns={"AIC":"AIC_FIGARCH","BIC":"BIC_FIGARCH"}
)

model_compare_df = (
    garch_df
    .merge(egarch_df,on="Ticker")
    .merge(gjr_df,on="Ticker")
    .merge(figarch_df,on="Ticker")
)

aic_cols = [
    "AIC_GARCH","AIC_EGARCH","AIC_GJR","AIC_FIGARCH"
]

model_compare_df["Best_Model"] = (
    model_compare_df[aic_cols].idxmin(axis=1)
    .str.replace("AIC_","")
)

model_compare_df.to_csv(
    "model_comparison_summary.csv",
    index=False
)

model_compare_df
