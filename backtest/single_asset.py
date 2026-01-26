import matplotlib
matplotlib.use("Agg")   # non-GUI backend (SAFE)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from regime.volatility_regime import detect_volatility_regime
from regime.regime_rules import regime_position_multiplier
from strategy.return_vol_signal import compute_return_vol_signal


# -------------------------------------------------
# SINGLE ASSET BACKTEST
# -------------------------------------------------

def run_single_asset_backtest(
    returns_df,
    garch_result,
    stock="INFY.NS",
    target_vol=0.01
):
    """
    Volatility + Regime + Return/Vol based strategy
    (NO look-ahead, production safe)
    """

    # -----------------------------------
    # STEP 1: Prepare returns
    # -----------------------------------
    backtest_df = (
        returns_df.loc[
            returns_df["Ticker"] == stock,
            ["Date", "log_return"]
        ]
        .dropna()
        .reset_index(drop=True)
    )

    # -----------------------------------
    # STEP 2: Attach GARCH volatility (ALIGN SAFELY)
    # -----------------------------------
    vol = (
        pd.Series(garch_result.conditional_volatility)
        .replace([np.inf, -np.inf], np.nan)
        .dropna()
        .values
    )

    vol = vol[-len(backtest_df):]  # strict alignment
    backtest_df["Forecasted_Volatility"] = vol

    # Use lagged volatility (NO look-ahead)
    backtest_df["Vol_Lag"] = backtest_df["Forecasted_Volatility"].shift(1)

    # Base position sizing
    backtest_df["Position_Size"] = (
        target_vol / backtest_df["Vol_Lag"]
    )

    backtest_df["Position_Size"] = backtest_df["Position_Size"].clip(0.1, 2.0)

    # -----------------------------------
    # STEP 3: Volatility Regime (LAGGED)
    # -----------------------------------
    backtest_df["Vol_Regime"] = detect_volatility_regime(
        backtest_df["Vol_Lag"]
    )

    backtest_df["Regime_Multiplier"] = backtest_df["Vol_Regime"].apply(
        regime_position_multiplier
    )

    backtest_df["Position_Size"] *= backtest_df["Regime_Multiplier"]

    # -----------------------------------
    # STEP 4: Return / Volatility Signal (LAGGED)
    # -----------------------------------
    backtest_df = compute_return_vol_signal(backtest_df)

    backtest_df["Signal"] = np.where(
        backtest_df["RV_Signal"].shift(1) > 0, 1, 0
    )

    # -----------------------------------
    # STEP 5: Strategy Returns
    # -----------------------------------
    backtest_df["Strategy_Return"] = (
        backtest_df["Signal"]
        * backtest_df["Position_Size"]
        * backtest_df["log_return"]
    )

    # Buy & Hold
    backtest_df["Buy_Hold_Return"] = backtest_df["log_return"]

    # -----------------------------------
    # STEP 6: Equity Curves
    # -----------------------------------
    backtest_df["Strategy_Equity"] = (
        1 + backtest_df["Strategy_Return"]
    ).cumprod()

    backtest_df["Buy_Hold_Equity"] = (
        1 + backtest_df["Buy_Hold_Return"]
    ).cumprod()

    # Final safety clean
    backtest_df = backtest_df.dropna()

    return backtest_df


# -------------------------------------------------
# PERFORMANCE METRICS
# -------------------------------------------------

def compute_performance_metrics(backtest_df):
    trading_days = 252
    eps = 1e-8

    equity = backtest_df["Strategy_Equity"]

    ann_return = equity.iloc[-1] ** (
        trading_days / len(equity)
    ) - 1

    ann_vol = (
        backtest_df["Strategy_Return"].std()
        * np.sqrt(trading_days)
    )

    sharpe = ann_return / (ann_vol + eps)

    max_dd = (
        equity / equity.cummax() - 1
    ).min()

    return pd.DataFrame({
        "Metric": [
            "Annual Return",
            "Annual Volatility",
            "Sharpe Ratio",
            "Max Drawdown"
        ],
        "Strategy": [
            ann_return,
            ann_vol,
            sharpe,
            max_dd
        ]
    })


# -------------------------------------------------
# PLOT
# -------------------------------------------------

def plot_equity_curve(backtest_df, stock="INFY.NS"):
    backtest_df["Date"] = pd.to_datetime(backtest_df["Date"])

    plt.figure(figsize=(12, 5))

    plt.plot(
        backtest_df["Date"],
        backtest_df["Strategy_Equity"],
        label="Strategy",
        linewidth=2
    )

    plt.plot(
        backtest_df["Date"],
        backtest_df["Buy_Hold_Equity"],
        label="Buy & Hold",
        linestyle="--"
    )

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    plt.title(f"Strategy vs Buy & Hold ({stock})")
    plt.xlabel("Date")
    plt.ylabel("Equity")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    import os
    os.makedirs("outputs/charts", exist_ok=True)
    path = f"outputs/charts/{stock}_single_asset_equity.png"
    plt.savefig(path, dpi=150)
    plt.close()

    print(f" Equity curve saved → {path}")


# -------------------------------------------------
# RUN SCRIPT
# -------------------------------------------------

if __name__ == "__main__":

    from models.egarch import fit_egarch
    from scripts.preprocess import load_returns_data

    returns_df = load_returns_data()
    stock = "INFY.NS"

    series = (
        returns_df.loc[
            returns_df["Ticker"] == stock,
            "log_return"
        ]
        .dropna()
        .values
    )

    egarch_result = fit_egarch(series)

    backtest_df = run_single_asset_backtest(
        returns_df,
        egarch_result,
        stock
    )
    print("\n FINAL SANITY CHECK\n")

    print(
        backtest_df[
            [
                "log_return",
                "Vol_Lag",
                "RV_Signal",
                "Signal",
                "Position_Size",
                "Strategy_Return"
            ]
        ].describe()
    )


    print("\n Volatility Regime Distribution\n")
    print(backtest_df["Vol_Regime"].value_counts())

    performance = compute_performance_metrics(backtest_df)
    print("\n PERFORMANCE SUMMARY\n")
    print(performance)

    plot_equity_curve(backtest_df, stock)
