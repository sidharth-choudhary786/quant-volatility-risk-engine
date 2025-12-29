def select_best_model(model_df):
    """
    Select model using:
    1️⃣ Lowest AIC
    2️⃣ Stability filter (persistence < 0.98)
    """

    # Drop unstable models
    stable_df = model_df.copy()

    stable_df = stable_df[
        (stable_df["Persistence"].isna()) |
        (stable_df["Persistence"] < 0.98)
    ]

    # If everything unstable → fallback
    if stable_df.empty:
        stable_df = model_df

    # Select lowest AIC
    best_row = stable_df.sort_values("AIC").iloc[0]

    return best_row["Model"], best_row["Result"]
