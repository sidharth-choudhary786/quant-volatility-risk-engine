import pandas as pd
import matplotlib.pyplot as plt

import os

def compare_portfolios():
    base_path = "outputs/final"

    baseline = pd.read_csv(
        f"{base_path}/portfolio_performance.csv"
    )

    regime = pd.read_csv(
        f"{base_path}/portfolio_regime_metrics.csv"
    )

    baseline["Portfolio"] = "Baseline"
    regime["Portfolio"] = "Regime-Aware"

    comparison = pd.concat(
        [baseline, regime],
        ignore_index=True
    )

    pivot = comparison.pivot(
        index="Metric",
        columns="Portfolio",
        values="Value"
    )

    os.makedirs(base_path, exist_ok=True)

    pivot.to_csv(
        f"{base_path}/portfolio_comparison.csv"
    )

    print("\n📊 PORTFOLIO COMPARISON\n")
    print(pivot)

    print(
        "\n✅ Comparison saved → outputs/final/portfolio_comparison.csv"
    )
        # -----------------------------
    # LOAD EQUITY DATA FOR PLOT
    # -----------------------------
    baseline_equity = pd.read_csv(
        f"{base_path}/portfolio_equity.csv"
    )

    regime_equity = pd.read_csv(
        f"{base_path}/portfolio_regime_equity.csv"
    )

    plot_portfolio_equity_comparison(
        baseline_equity,
        regime_equity
    )

# =====================================================
# PLOT: BASELINE vs REGIME PORTFOLIO EQUITY
# =====================================================

def plot_portfolio_equity_comparison(baseline_df, regime_df):
    """
    Plots equity curve comparison between
    baseline portfolio and regime-aware portfolio
    """

    plt.figure(figsize=(12, 5))

    plt.plot(
        baseline_df["Portfolio_Equity"],
        label="Baseline Portfolio",
        linewidth=2
    )

    plt.plot(
        regime_df["Portfolio_Equity"],
        label="Regime-Aware Portfolio",
        linewidth=2
    )

    plt.title("Baseline vs Regime-Aware Portfolio Equity Curve")
    plt.xlabel("Time")
    plt.ylabel("Equity")
    plt.grid(True)
    plt.legend()

    os.makedirs("outputs/charts", exist_ok=True)
    plt.tight_layout()
    plt.savefig(
        "outputs/charts/portfolio_equity_comparison.png",
        dpi=150
    )
    plt.close()

    print("📈 Portfolio equity comparison plot saved → outputs/charts/portfolio_equity_comparison.png")

if __name__ == "__main__":
    compare_portfolios()
