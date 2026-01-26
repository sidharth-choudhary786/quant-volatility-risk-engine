import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------
# WALK-FORWARD OUT-OF-SAMPLE BACKTEST
# -------------------------------------------------

def run_walk_forward_backtest(
    df,
    train_years=3,
    test_years=1
):
    """
    Walk-forward validation using FIXED strategy rules.
    NO refitting, NO logic change.
    """

    data = df.copy()

    data["Date"] = pd.to_datetime(data["Date"])
    data["Year"] = data["Date"].dt.year

    years = sorted(data["Year"].unique())

    walkforward_results = []

    # -----------------------------------
    # WALK-FORWARD LOOP
    # -----------------------------------
    for i in range(len(years) - train_years - test_years + 1):

        train_start = years[i]
        train_end   = years[i + train_years - 1]
        test_year   = years[i + train_years]

        # Training data (NOT used directly, kept for structure integrity)
        train_df = data[
            (data["Year"] >= train_start) &
            (data["Year"] <= train_end)
        ].copy()

        # Testing data
        test_df = data[data["Year"] == test_year].copy()

        # Safety checks
        if len(train_df) < 252 or len(test_df) < 50:
            continue

        # -----------------------------------
        # STRATEGY RULES
        # -----------------------------------
        test_df["Signal"] = np.where(
            (test_df["Price"] > test_df["MA_Price"]) &
            (
                test_df["Forecasted_Volatility"]
                < test_df["Forecasted_Volatility"].rolling(60).median()
            ),
            1,
            0
        )

        test_df["Strategy_Return_Test"] = (
            test_df["Signal"]
            * test_df["Position_Size"]
            * test_df["log_return"]
        )

        # -----------------------------------
        # PERFORMANCE METRICS
        # -----------------------------------
        equity = (1 + test_df["Strategy_Return_Test"]).cumprod()

        ann_return = equity.iloc[-1] ** (252 / len(equity)) - 1
        ann_vol = test_df["Strategy_Return_Test"].std() * np.sqrt(252)

        sharpe = ann_return / ann_vol if ann_vol != 0 else np.nan

        walkforward_results.append({
            "Train_Period": f"{train_start}-{train_end}",
            "Test_Year": test_year,
            "Annual Return": ann_return,
            "Annual Volatility": ann_vol,
            "Sharpe Ratio": sharpe
        })

    return pd.DataFrame(walkforward_results)


# ---------------
# PLOT FUNCTION
# ---------------

def plot_walk_forward_sharpe(walkforward_df):
    """
    Visual check for out-of-sample Sharpe stability.
    """

    if walkforward_df.empty:
        print("No walk-forward results to plot.")
        return

    walkforward_df.plot(
        x="Test_Year",
        y="Sharpe Ratio",
        marker="o",
        figsize=(10, 4),
        title="Walk-Forward Out-of-Sample Sharpe Ratio"
    )

    plt.grid(True)
    plt.tight_layout()
    plt.show()

