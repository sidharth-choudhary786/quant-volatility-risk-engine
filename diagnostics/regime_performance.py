import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def regime_performance(backtest_df):
    results = []

    for regime, df in backtest_df.groupby("Vol_Regime"):
        if len(df) < 50:
            continue

        equity = (1 + df["Strategy_Return"]).cumprod()

        ann_ret = equity.iloc[-1] ** (252 / len(df)) - 1
        ann_vol = df["Strategy_Return"].std() * np.sqrt(252)
        sharpe = ann_ret / (ann_vol + 1e-8)
        max_dd = (equity / equity.cummax() - 1).min()

        results.append({
            "Regime": regime,
            "Annual Return": ann_ret,
            "Annual Volatility": ann_vol,
            "Sharpe": sharpe,
            "Max Drawdown": max_dd,
            "Observations": len(df)
        })

    return pd.DataFrame(results)


# =====================================================
# PLOT: VOLATILITY REGIME DISTRIBUTION
# =====================================================


def plot_regime_distribution(backtest_df):
    """
    Bar plot of volatility regime frequency
    """

    regime_counts = (
        backtest_df["Vol_Regime"]
        .value_counts()
        .sort_index()
    )

    plt.figure(figsize=(8, 5))
    regime_counts.plot(
        kind="bar",
        color=["green", "orange", "red", "gray"]
    )

    plt.title("Volatility Regime Distribution")
    plt.xlabel("Regime")
    plt.ylabel("Number of Observations")
    plt.grid(axis="y", alpha=0.3)

    os.makedirs("outputs/charts", exist_ok=True)
    plt.tight_layout()
    plt.savefig(
        "outputs/charts/regime_distribution.png",
        dpi=150
    )
    plt.close()

    print("📊 Regime distribution plot saved → outputs/charts/regime_distribution.png")
