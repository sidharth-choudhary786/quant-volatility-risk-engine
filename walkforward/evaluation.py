import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os

def evaluate_walkforward(df, save_path="outputs/final/walkforward_metrics.csv"):
    """
    Evaluate TRUE rolling walk-forward results.
    Fully safe, reviewer-grade implementation.
    """

    trading_days = 252
    eps = 1e-8  # numerical safety

    # -----------------------------
    # 1️⃣ Clean safety
    # -----------------------------
    returns = (
        df["Strategy_Return"]
        .replace([np.inf, -np.inf], np.nan)
        .dropna()
    )

    if len(returns) < 50:
        raise ValueError("Not enough walk-forward data to evaluate")

    # -----------------------------
    # 2️⃣ Equity (normalized)
    # -----------------------------
    equity = (1 + returns).cumprod()
    equity = equity / equity.iloc[0]   #  normalization

    # -----------------------------
    # 3️⃣ Metrics
    # -----------------------------
    ann_return = equity.iloc[-1] ** (
        trading_days / len(equity)
    ) - 1

    ann_vol = returns.std() * np.sqrt(trading_days)

    sharpe = ann_return / (ann_vol + eps)

    max_dd = (
        equity / equity.cummax() - 1
    ).min()

    metrics = {
        "Annual Return": ann_return,
        "Annual Volatility": ann_vol,
        "Sharpe Ratio": sharpe,
        "Max Drawdown": max_dd
    }

    # -----------------------------
    # 4️⃣ Save result (CRITICAL)
    # -----------------------------
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    pd.DataFrame([metrics]).to_csv(
        save_path,
        index=False
    )

    print(f"----- Walk-forward metrics saved → {save_path}")

    return metrics


# =====================================================
# PLOT: WALK-FORWARD EQUITY CURVE
# =====================================================


def plot_walkforward_equity(df):
    """
    Plots walk-forward strategy equity curve
    (NO look-ahead, cumulative performance)
    """

    equity = (1 + df["Strategy_Return"]).cumprod()

    plt.figure(figsize=(12, 5))
    plt.plot(df["Date"], equity, label="Walk-Forward Equity")
    plt.title("Walk-Forward Strategy Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Equity")
    plt.grid(True)
    plt.legend()

    os.makedirs("outputs/charts", exist_ok=True)
    plt.savefig(
        "outputs/charts/walkforward_equity.png",
        dpi=150
    )
    plt.close()

    print("📈 Walk-forward equity plot saved → outputs/charts/walkforward_equity.png")



if __name__ == "__main__":
    from walkforward.run_walkforward import run_walkforward
    from scripts.preprocess import load_returns_data

    returns_df = load_returns_data()
    wf_df = run_walkforward(returns_df)

    metrics = evaluate_walkforward(wf_df)
    print(metrics)
    plot_walkforward_equity(wf_df)
