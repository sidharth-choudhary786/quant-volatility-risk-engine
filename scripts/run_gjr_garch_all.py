import pandas as pd
import numpy as np
from arch import arch_model
from tqdm import tqdm

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

RETURNS_PATH = "nifty50_history_with_adj/nifty50_log_returns_clean.csv"
OUTPUT_PATH  = "outputs/gjr_garch_results_50stocks.csv"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

returns_df = pd.read_csv(RETURNS_PATH)

tickers = sorted(returns_df["Ticker"].unique())

# --------------------------------------------------
# GJR-GARCH FUNCTION (SAME AS YOUR CODE)
# --------------------------------------------------

def fit_gjr_garch(series):
    model = arch_model(
        series,
        mean="Constant",
        vol="GARCH",
        p=1,
        o=1,          # <-- GJR asymmetry term
        q=1,
        dist="normal",
        rescale=False
    )
    return model.fit(disp="off")

# --------------------------------------------------
# RUN FOR ALL STOCKS
# --------------------------------------------------

results = []
failed  = []

print("\nRunning GJR-GARCH(1,1) for ALL stocks...\n")

for ticker in tqdm(tickers):
    try:
        series = returns_df.loc[
            returns_df["Ticker"] == ticker,
            "log_return"
        ].values

        result = fit_gjr_garch(series)

        omega = result.params["omega"]
        alpha = result.params["alpha[1]"]
        beta  = result.params["beta[1]"]
        gamma = result.params["gamma[1]"]

        # Fear-adjusted persistence (IMPORTANT)
        persistence = alpha + beta + 0.5 * gamma

        results.append({
            "Ticker": ticker,
            "omega": omega,
            "alpha": alpha,
            "beta": beta,
            "gamma": gamma,                  # 🔥 crisis fear
            "persistence": persistence,      # 🔥 crisis memory
            "AIC": result.aic,
            "BIC": result.bic
        })

    except Exception as e:
        failed.append(ticker)
        print(f"❌ Failed for {ticker}: {e}")

# --------------------------------------------------
# SAVE OUTPUT
# --------------------------------------------------

results_df = pd.DataFrame(results)

results_df.to_csv(OUTPUT_PATH, index=False)

print("\n✅ GJR-GARCH batch run completed")
print(f"📄 Output saved to: {OUTPUT_PATH}")

if failed:
    print("\n⚠️ Failed stocks:")
    print(failed)
else:
    print("\n🎉 All stocks processed successfully")
