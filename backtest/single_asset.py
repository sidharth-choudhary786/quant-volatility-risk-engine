import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# -------------------------------------------------
# SINGLE ASSET BACKTEST (INFY.NS)
# -------------------------------------------------

def run_single_asset_backtest(
    returns_df,
    garch_result,
    stock="INFY.NS",
    target_vol=0.01
):
    """
    Runs volatility-targeted backtest for ONE stock.
    Logic exactly same as your notebook.
    """

    # -----------------------------------
    # STEP 1: Prepare price return data
    # -----------------------------------
    stock_returns = returns_df.loc[
        returns_df["Ticker"] == stock,
        ["Date", "log_return"]
    ].reset_index(drop=True)

    backtest_df = stock_returns.copy()

    # -----------------------------------
    # STEP 2: Attach volatility & position size
    # -----------------------------------
    backtest_df["Forecasted_Volatility"] = garch_result.conditional_volatility

    backtest_df["Position_Size"] = (
        target_vol / backtest_df["Forecasted_Volatility"]
    ).clip(0.1, 2.0)

    # -----------------------------------
    # STEP 3: Trading signal (momentum)
    # -----------------------------------
    backtest_df["Signal"] = np.where(
        backtest_df["log_return"].shift(1) > 0, 1, 0
    )

    # -----------------------------------
    # STEP 4: Strategy returns
    # -----------------------------------
    backtest_df["Strategy_Return"] = (
        backtest_df["Signal"]
        * backtest_df["Position_Size"]
        * backtest_df["log_return"]
    )

    # -----------------------------------
    # STEP 5: Buy & Hold
    # -----------------------------------
    backtest_df["Buy_Hold_Return"] = backtest_df["log_return"]

    # -----------------------------------
    # STEP 6: Equity curves
    # -----------------------------------
    backtest_df["Strategy_Equity"] = (
        1 + backtest_df["Strategy_Return"]
    ).cumprod()

    backtest_df["Buy_Hold_Equity"] = (
        1 + backtest_df["Buy_Hold_Return"]
    ).cumprod()

    return backtest_df


# -------------------------------------------------
# PERFORMANCE METRICS (same as your code 10 & 12)
# -------------------------------------------------

def compute_performance_metrics(backtest_df):
    trading_days = 252

    strategy_ann_return = (
        backtest_df["Strategy_Equity"].iloc[-1]
        ** (trading_days / len(backtest_df))
        - 1
    )

    buyhold_ann_return = (
        backtest_df["Buy_Hold_Equity"].iloc[-1]
        ** (trading_days / len(backtest_df))
        - 1
    )

    strategy_ann_vol = (
        backtest_df["Strategy_Return"].std()
        * np.sqrt(trading_days)
    )

    buyhold_ann_vol = (
        backtest_df["Buy_Hold_Return"].std()
        * np.sqrt(trading_days)
    )

    strategy_sharpe = strategy_ann_return / strategy_ann_vol
    buyhold_sharpe = buyhold_ann_return / buyhold_ann_vol

    strategy_dd = (
        backtest_df["Strategy_Equity"]
        / backtest_df["Strategy_Equity"].cummax()
        - 1
    ).min()

    buyhold_dd = (
        backtest_df["Buy_Hold_Equity"]
        / backtest_df["Buy_Hold_Equity"].cummax()
        - 1
    ).min()

    performance_df = pd.DataFrame({
        "Metric": [
            "Annual Return",
            "Annual Volatility",
            "Sharpe Ratio",
            "Max Drawdown"
        ],
        "Strategy": [
            strategy_ann_return,
            strategy_ann_vol,
            strategy_sharpe,
            strategy_dd
        ],
        "Buy & Hold": [
            buyhold_ann_return,
            buyhold_ann_vol,
            buyhold_sharpe,
            buyhold_dd
        ]
    })

    return performance_df


# -------------------------------------------------
# PLOT FUNCTION (same visuals)
# -------------------------------------------------

def plot_equity_curve(backtest_df, stock="INFY.NS"):
    backtest_df["Date"] = pd.to_datetime(backtest_df["Date"])

    plt.figure(figsize=(12, 5))

    plt.plot(
        backtest_df["Date"],
        backtest_df["Strategy_Equity"],
        label="Volatility Targeted Strategy",
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
    plt.ylabel("Equity Curve")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

