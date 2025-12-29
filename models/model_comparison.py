import pandas as pd
import numpy as np

# --------------------------------------------------
# PATHS
# --------------------------------------------------

GARCH_PATH  = "outputs/garch_results_50stocks.csv"
EGARCH_PATH = "outputs/egarch_results_50stocks.csv"
GJR_PATH    = "outputs/gjr_garch_results_50stocks.csv"

OUTPUT_PATH = "outputs/model_comparison_summary.csv"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

garch_df  = pd.read_csv(GARCH_PATH)
egarch_df = pd.read_csv(EGARCH_PATH)
gjr_df    = pd.read_csv(GJR_PATH)

# --------------------------------------------------
# KEEP ONLY COMPARISON COLUMNS
# --------------------------------------------------

garch_df = garch_df[["Ticker", "AIC", "BIC"]].rename(
    columns={"AIC": "AIC_GARCH", "BIC": "BIC_GARCH"}
)

egarch_df = egarch_df[["Ticker", "AIC", "BIC"]].rename(
    columns={"AIC": "AIC_EGARCH", "BIC": "BIC_EGARCH"}
)

gjr_df = gjr_df[["Ticker", "AIC", "BIC"]].rename(
    columns={"AIC": "AIC_GJR", "BIC": "BIC_GJR"}
)

# --------------------------------------------------
# MERGE ALL MODELS
# --------------------------------------------------

compare_df = (
    garch_df
    .merge(egarch_df, on="Ticker")
    .merge(gjr_df, on="Ticker")
)

# --------------------------------------------------
# SELECT BEST MODEL (LOWEST AIC)
# --------------------------------------------------

aic_cols = ["AIC_GARCH", "AIC_EGARCH", "AIC_GJR"]

compare_df["Best_Model"] = compare_df[aic_cols].idxmin(axis=1)
compare_df["Best_Model"] = compare_df["Best_Model"].str.replace("AIC_", "")

# --------------------------------------------------
# OPTIONAL: SECONDARY CHECK USING BIC
# --------------------------------------------------

bic_cols = ["BIC_GARCH", "BIC_EGARCH", "BIC_GJR"]

compare_df["Best_Model_BIC"] = compare_df[bic_cols].idxmin(axis=1)
compare_df["Best_Model_BIC"] = compare_df["Best_Model_BIC"].str.replace("BIC_", "")

# --------------------------------------------------
# SAVE OUTPUT
# --------------------------------------------------

compare_df.to_csv(OUTPUT_PATH, index=False)

print("\n✅ Model comparison completed")
print(f"📄 Output saved to: {OUTPUT_PATH}")

# --------------------------------------------------
# QUICK SUMMARY
# --------------------------------------------------

print("\n📊 Best model count (AIC-based):")
print(compare_df["Best_Model"].value_counts())

print("\n📊 Best model count (BIC-based):")
print(compare_df["Best_Model_BIC"].value_counts())
