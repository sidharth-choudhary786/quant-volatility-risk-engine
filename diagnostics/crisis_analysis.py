def crisis_window(df, start, end):
    crisis = df[
        (df["Date"] >= start) &
        (df["Date"] <= end)
    ].copy()

    equity = (1 + crisis["Strategy_Return"]).cumprod()

    return {
        "Start": start,
        "End": end,
        "Max Drawdown": (equity / equity.cummax() - 1).min(),
        "Volatility": crisis["Strategy_Return"].std() * (252**0.5)
    }
# =====================================================
# PLOT: CRISIS EQUITY CURVE
# =====================================================

import matplotlib.pyplot as plt
import os

def plot_crisis_equity(backtest_df, start_date, end_date, label):
    """
    Plots equity curve during a crisis window
    """

    crisis_df = backtest_df[
        (backtest_df["Date"] >= start_date) &
        (backtest_df["Date"] <= end_date)
    ].copy()

    if crisis_df.empty:
        return

    equity = (1 + crisis_df["Strategy_Return"]).cumprod()

    plt.figure(figsize=(10, 4))
    plt.plot(crisis_df["Date"], equity, linewidth=2)

    plt.title(f"Equity Curve During {label}")
    plt.xlabel("Date")
    plt.ylabel("Equity")
    plt.grid(True)

    os.makedirs("outputs/charts", exist_ok=True)

    filename = f"outputs/charts/crisis_{label.replace(' ', '_').lower()}.png"
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()

    print(f"📉 Crisis equity plot saved → {filename}")
