import pandas as pd
import numpy as np

def apply_risk_allocator(
    portfolio_df,
    portfolio_returns
):
    """
    Adjusts portfolio exposure using risk constraint
    """

    from risk_allocator.allocator import risk_constrained_scaler

    # Safety clean
    clean_returns = (
        pd.Series(portfolio_returns)
        .replace([np.inf, -np.inf], np.nan)
        .dropna()
        .values
    )

    scale, var, es = risk_constrained_scaler(clean_returns)

    portfolio_df = portfolio_df.copy()

    # Apply scaling
    portfolio_df["Risk_Scale"] = scale

    portfolio_df["Adj_Return"] = (
        portfolio_df["Portfolio_Return"] * scale
    )

    portfolio_df["Adj_Equity"] = (
        1 + portfolio_df["Adj_Return"]
    ).cumprod()

    return portfolio_df, {
        "Portfolio_VaR": var,
        "Portfolio_ES": es,
        "Risk_Scale": scale
    }
if __name__ == "__main__":
    import numpy as np
    import pandas as pd

    np.random.seed(0)
    returns = np.random.normal(0, 0.01, 1000)

    df = pd.DataFrame({"Portfolio_Return": returns})

    df_out, summary = apply_risk_allocator(df, df["Portfolio_Return"])

    print("\nSELF TEST – RISK ALLOCATOR\n")
    print(summary)
