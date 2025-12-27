import numpy as np
import pandas as pd
import os

# =====================================================
# PORTFOLIO BACKTEST (10 STOCKS)
# =====================================================

def run_portfolio_backtest(returns_df, portfolio_stocks):
    """
    Runs inverse-volatility weighted portfolio backtest
    """

    # -----------------------------------
    # Create return matrix
    # -----------------------------------
    portfolio_df = returns_df[
        returns_df["Ticker"].isin(portfolio_stocks)
    ].pivot(
        index="Date",
        columns="Ticker",
        values="log_return"
    ).dropna()

    # -----------------------------------
    # Rolling volatility (proxy for GARCH)
    # -----------------------------------
    rolling_window = 60
    vol_df = portfolio_df.rolling(rolling_window).std()

    # -----------------------------------
    # Inverse volatility weights
    # -----------------------------------
    inv_vol = 1 / vol_df
    weights = inv_vol.div(inv_vol.sum(axis=1), axis=0)

    # -----------------------------------
    # Portfolio returns & equity
    # -----------------------------------
    portfolio_returns = (weights * portfolio_df).sum(axis=1)
    portfolio_equity = (1 + portfolio_returns).cumprod()

    return portfolio_returns, portfolio_equity


# =====================================================
# PORTFOLIO PERFORMANCE METRICS
# =====================================================

def portfolio_performance_metrics(portfolio_returns, portfolio_equity):
    trading_days = 252

    ann_return = (
        portfolio_equity.iloc[-1]
        ** (trading_days / len(portfolio_equity))
        - 1
    )

    ann_vol = portfolio_returns.std() * np.sqrt(trading_days)
    sharpe = ann_return / ann_vol

    max_dd = (
        portfolio_equity
        / portfolio_equity.cummax()
        - 1
    ).min()

    return {
        "Annual Return": ann_return,
        "Annual Volatility": ann_vol,
        "Sharpe Ratio": sharpe,
        "Max Drawdown": max_dd
    }


# =====================================================
# PORTFOLIO RISK (VaR, ES, DIVERSIFICATION)
# =====================================================

def portfolio_risk_metrics(returns_df, portfolio_returns):
    trading_days = 252

    # -------- Historical VaR / ES --------
    alpha_95 = 0.05
    alpha_99 = 0.01

    var_95 = abs(np.percentile(portfolio_returns.dropna(), alpha_95 * 100))
    es_95 = abs(portfolio_returns[portfolio_returns <= -var_95].mean())

    var_99 = abs(np.percentile(portfolio_returns.dropna(), alpha_99 * 100))
    es_99 = abs(portfolio_returns[portfolio_returns <= -var_99].mean())

    # -------- Annualized --------
    var_annual = var_95 * np.sqrt(trading_days)
    es_annual = es_95 * np.sqrt(trading_days)

    # -------- Diversification --------
    individual_var = (
        returns_df
        .groupby("Ticker")["log_return"]
        .apply(lambda x: abs(np.percentile(x, 5)))
    )

    diversification_benefit = 1 - var_95 / individual_var.mean()

    return {
        "VaR_95": var_95,
        "ES_95": es_95,
        "VaR_99": var_99,
        "ES_99": es_99,
        "Annual_VaR": var_annual,
        "Annual_ES": es_annual,
        "Diversification_Benefit": diversification_benefit
    }


# =====================================================
# SAVE RESULTS
# =====================================================

def save_portfolio_outputs(metrics_dict, output_dir="phase4_outputs"):
    os.makedirs(output_dir, exist_ok=True)

    pd.DataFrame(
        list(metrics_dict.items()),
        columns=["Metric", "Value"]
    ).to_csv(
        f"{output_dir}/portfolio_risk_metrics.csv",
        index=False
    )

