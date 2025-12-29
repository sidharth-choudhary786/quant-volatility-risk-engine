import numpy as np
import pandas as pd

# -------------------------------------------------
# PORTFOLIO-LEVEL RISK
# VaR, ES & Diversification
# -------------------------------------------------

def compute_portfolio_risk(
    returns_df,
    portfolio_stocks,
    confidence_levels=(0.95, 0.99)
):
    """
    Computes portfolio-level:
    - Historical VaR
    - Expected Shortfall
    - Annualized Risk
    - Diversification Benefit

    Logic EXACTLY SAME as Code 16
    Only index alignment fixes applied
    """

    # -----------------------------------
    # STEP 1: Prepare aligned return matrix
    # -----------------------------------
    portfolio_df = (
        returns_df[
            returns_df["Ticker"].isin(portfolio_stocks)
        ]
        .pivot(
            index="Date",
            columns="Ticker",
            values="log_return"
        )
        .dropna()
    )

    # -----------------------------------
    # STEP 2: Equal-weight portfolio
    # -----------------------------------
    n_assets = portfolio_df.shape[1]
    weights = np.repeat(1 / n_assets, n_assets)

    portfolio_returns = portfolio_df.dot(weights)

    trading_days = 252
    risk_summary = []

    # -----------------------------------
    # STEP 3: VaR & ES for each confidence level
    # -----------------------------------
    for cl in confidence_levels:
        alpha = 1 - cl

        # Historical VaR
        var = abs(
            np.percentile(
                portfolio_returns.values,
                alpha * 100
            )
        )

        # Expected Shortfall
        es = abs(
            portfolio_returns[
                portfolio_returns <= -var
            ].mean()
        )

        # Annualized
        var_annual = var * np.sqrt(trading_days)
        es_annual = es * np.sqrt(trading_days)

        risk_summary.append({
            "Confidence_Level": cl,
            "VaR": var,
            "ES": es,
            "Annualized_VaR": var_annual,
            "Annualized_ES": es_annual
        })

    risk_df = pd.DataFrame(risk_summary)

    # -----------------------------------
    # STEP 4: Diversification Benefit (aligned universe)
    # -----------------------------------
    aligned_returns = returns_df[
        returns_df["Date"].isin(portfolio_df.index)
        & returns_df["Ticker"].isin(portfolio_stocks)
    ]

    individual_var = (
        aligned_returns
        .groupby("Ticker")["log_return"]
        .apply(lambda x: abs(np.percentile(x, 5)))
    )

    portfolio_var_95 = risk_df.loc[
        risk_df["Confidence_Level"] == 0.95,
        "VaR"
    ].values[0]

    diversification_benefit = (
        1 - portfolio_var_95 / individual_var.mean()
    )

    diversification_df = pd.DataFrame({
        "Metric": [
            "Average Individual VaR",
            "Portfolio VaR (95%)",
            "Diversification Benefit"
        ],
        "Value": [
            individual_var.mean(),
            portfolio_var_95,
            diversification_benefit
        ]
    })

    # -----------------------------------
    # FINAL OUTPUT
    # -----------------------------------
    return {
        "Portfolio_Returns": portfolio_returns,
        "Risk_Metrics": risk_df,
        "Diversification": diversification_df
    }
