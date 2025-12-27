import numpy as np
import pandas as pd

# -------------------------------------------------
# PORTFOLIO RISK
# VaR, ES & DIVERSIFICATION BENEFIT
# -------------------------------------------------

def compute_portfolio_risk(
    returns_df,
    portfolio_stocks,
    confidence_levels=(0.95, 0.99)
):
    """
    Portfolio-level risk:
    - Historical VaR & ES
    - Annualized risk
    - Diversification benefit

    Logic EXACTLY SAME as Code 16
    """

    # -----------------------------------
    # Prepare portfolio returns
    # -----------------------------------
    portfolio_df = returns_df[
        returns_df["Ticker"].isin(portfolio_stocks)
    ]

    returns_matrix = portfolio_df.pivot(
        index="Date",
        columns="Ticker",
        values="log_return"
    )

    n_assets = returns_matrix.shape[1]
    weights = np.repeat(1 / n_assets, n_assets)

    portfolio_returns = returns_matrix.dot(weights).dropna()

    results = {}

    for cl in confidence_levels:
        alpha = 1 - cl

        var = abs(np.percentile(portfolio_returns, alpha * 100))
        es = abs(
            portfolio_returns[
                portfolio_returns <= -var
            ].mean()
        )

        results[f"VaR_{int(cl*100)}"] = var
        results[f"ES_{int(cl*100)}"] = es

    # -----------------------------------
    # Diversification benefit
    # -----------------------------------
    individual_var = (
        returns_df
        .groupby("Ticker")["log_return"]
        .apply(lambda x: abs(np.percentile(x, 5)))
    )

    diversification_benefit = (
        1 - results["VaR_95"] / individual_var.mean()
    )

    # -----------------------------------
    # Final summary
    # -----------------------------------
    portfolio_risk_summary = pd.DataFrame({
        "Metric": [
            "Portfolio VaR (95%)",
            "Portfolio ES (95%)",
            "Portfolio VaR (99%)",
            "Portfolio ES (99%)",
            "Diversification Benefit"
        ],
        "Value": [
            results["VaR_95"],
            results["ES_95"],
            results["VaR_99"],
            results["ES_99"],
            diversification_benefit
        ]
    })

    return portfolio_risk_summary
