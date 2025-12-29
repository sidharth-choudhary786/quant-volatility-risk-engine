import pandas as pd
import numpy as np

from walkforward.config import (
    STOCK,
    TRAIN_YEARS,
    TEST_MONTHS,
    TARGET_VOL
)

from walkforward.rolling_windows import generate_rolling_windows

# STEP–3: dynamic model switching
from model_switching.refit_models import refit_all_models
from model_switching.selector import select_best_model


def run_walkforward(returns_df):
    """
    TRUE Rolling Walk-Forward with:
    - re-fitting every window
    - dynamic volatility model selection
    - NO look-ahead bias
    """

    # -----------------------------------
    # Filter single stock
    # -----------------------------------
    stock_df = returns_df[
        returns_df["Ticker"] == STOCK
    ].copy()

    stock_df["Date"] = pd.to_datetime(stock_df["Date"])

    # -----------------------------------
    # Generate rolling windows
    # -----------------------------------
    windows = generate_rolling_windows(
        dates=stock_df["Date"],
        train_years=TRAIN_YEARS,
        test_months=TEST_MONTHS
    )

    all_results = []

    # -----------------------------------
    # Walk-forward loop
    # -----------------------------------
    for window_id, (tr_start, tr_end, te_start, te_end) in enumerate(windows):

        # -------------------------------
        # Train / Test split
        # -------------------------------
        train_df = stock_df[
            (stock_df["Date"] >= tr_start) &
            (stock_df["Date"] < tr_end)
        ]

        test_df = stock_df[
            (stock_df["Date"] >= te_start) &
            (stock_df["Date"] < te_end)
        ]

        # Safety guards
        if len(train_df) < 500 or len(test_df) < 20:
            continue

        # -------------------------------
        # CLEAN TRAINING SERIES
        # -------------------------------
        train_series = (
            train_df["log_return"]
            .replace([np.inf, -np.inf], np.nan)
            .dropna()
            .values
        )

        if len(train_series) < 300:
            continue

        # ==================================================
        # 🔥 STEP–3: REFIT ALL MODELS ON TRAIN WINDOW
        # ==================================================
        model_df = refit_all_models(train_series)

        best_model_name, best_model_result = select_best_model(model_df)

        # -------------------------------
        # Extract conditional volatility
        # -------------------------------
        vol_series = (
            pd.Series(best_model_result.conditional_volatility)
            .replace([np.inf, -np.inf], np.nan)
            .dropna()
        )

        # Align volatility with test window
        vol_series = vol_series.iloc[-len(test_df):].values

        test_df = test_df.copy()
        test_df["Forecasted_Volatility"] = vol_series
        test_df["Selected_Model"] = best_model_name

        # -------------------------------
        # Position sizing (STEP–2 untouched)
        # -------------------------------
        test_df["Position_Size"] = (
            TARGET_VOL / test_df["Forecasted_Volatility"]
        ).clip(0.1, 2.0)

        # -------------------------------
        # Trading signal (simple momentum)
        # -------------------------------
        test_df["Signal"] = np.where(
            test_df["log_return"].shift(1) > 0, 1, 0
        )

        # -------------------------------
        # Final safety cleaning
        # -------------------------------
        test_df = test_df.replace([np.inf, -np.inf], np.nan)
        test_df = test_df.dropna(
            subset=[
                "log_return",
                "Forecasted_Volatility",
                "Position_Size",
                "Signal"
            ]
        )

        # -------------------------------
        # Strategy return
        # -------------------------------
        test_df["Strategy_Return"] = (
            test_df["Signal"]
            * test_df["Position_Size"]
            * test_df["log_return"]
        )

        test_df["Window_ID"] = window_id

        all_results.append(test_df)

    # -----------------------------------
    # Combine all windows
    # -----------------------------------
    if len(all_results) == 0:
        raise ValueError("No valid walk-forward windows generated")

    return pd.concat(all_results, ignore_index=True)
