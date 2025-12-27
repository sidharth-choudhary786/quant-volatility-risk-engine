import os
import numpy as np
import pandas as pd

# -------------------------------------------------
# PORTFOLIO-LEVEL RISK (VaR, ES, Diversification)
# -------------------------------------------------

def run_portfolio_risk_analysis(
    returns_df,
    output_dir="phase4_outputs",
    confidence_levels=(0.95, 0.99),
    n_stocks=10
):
    """
    Portfolio risk analysis using:
    - Historical VaR
    - Historical Expected Shortfall
    - Annualized risk
    - Diversification benefit

    Logic EXACTLY SAME as Code 16.
    """

    # -----------------------------------
    # Select first N stocks (tested logic)
    # -----------------------------------
    portfolio_stocks = returns_df["Ticker"].unique()[:n_stocks]

    portfolio_df = returns_df[
        returns_df["Ticker"].isin(portfolio_stocks)
    ]

    # Pivot to Date × Stock matrix
    returns_matrix = portfolio_df.pivot(
        index="Date",
        columns="Ticker",
        values="log_return"
    )

    # -----------------------------------
    # Equal-weight portfolio
    # -----------------------------------
    n_assets = returns_matrix.shape[1]
    weights = np.repeat(1 / n_assets, n_assets)

    portfolio_returns = returns_matrix.dot(weights)

    # -----------------------------------
    # Risk calculations
    # -----------------------------------
    risk_results = {}

    for cl in confidence_levels:
        alpha = 1 - cl

        portfolio_var = abs(
            np.percentile(portfolio_returns.dropna(), alpha * 100)
        )

        portfolio_es = abs(
            portfolio_returns[
                portfolio_returns <= -portfolio_var
            ].mean()
        )

        risk_results[f"VaR_{int(cl*100)}"] = portfolio_var
        risk_results[f"ES_{int(cl*100)}"] = portfolio_es

    # -----------------------------------
    # Annualized risk
    # -----------------------------------
    trading_days = 252

    portfolio_var_annual = risk_results["VaR_95"] * np.sqrt(trading_days)
    portfolio_es_annual  = risk_results["ES_95"]  * np.sqrt(trading_days)

    # -----------------------------------
    # Individual stock risk
    # -----------------------------------
    individual_var = (
        returns_df
        .groupby("Ticker")["log_return"]
        .apply(lambda x: abs(np.percentile(x, 5)))
    )

    diversification_benefit = (
        1 - risk_results["VaR_95"] / individual_var.mean()
    )

    # -----------------------------------
    # Summary tables
    # -----------------------------------
    portfolio_risk_summary = pd.DataFrame({
        "Metric": [
            "Portfolio VaR (95%)",
            "Portfolio ES (95%)",
            "Avg Individual VaR",
            "Diversification Benefit"
        ],
        "Value": [
            f"{risk_results['VaR_95']*100:.2f}%",
            f"{risk_results['ES_95']*100:.2f}%",
            f"{individual_var.mean()*100:.2f}%",
            f"{diversification_benefit*100:.2f}%"
        ]
    })

    # -----------------------------------
    # Save outputs
    # -----------------------------------
    os.makedirs(output_dir, exist_ok=True)

    portfolio_risk_summary.to_csv(
        f"{output_dir}/portfolio_risk_summary.csv",
        index=False
    )

    pd.DataFrame({
        "Metric": [
            "Portfolio VaR 95%",
            "Portfolio ES 95%",
            "Portfolio VaR 99%",
            "Portfolio ES 99%",
            "Annual VaR",
            "Annual ES",
            "Diversification Benefit"
        ],
        "Value": [
            risk_results["VaR_95"],
            risk_results["ES_95"],
            risk_results["VaR_99"],
            risk_results["ES_99"],
            portfolio_var_annual,
            portfolio_es_annual,
            diversification_benefit
        ]
    }).to_csv(
        f"{output_dir}/risk_metrics_full.csv",
        index=False
    )

    return {
        "Portfolio_Returns": portfolio_returns,
        "VaR_95": risk_results["VaR_95"],
        "ES_95": risk_results["ES_95"],
        "VaR_99": risk_results["VaR_99"],
        "ES_99": risk_results["ES_99"],
        "Annual_VaR": portfolio_var_annual,
        "Annual_ES": portfolio_es_annual,
        "Diversification_Benefit": diversification_benefit,
        "Summary_Table": portfolio_risk_summary
    }

