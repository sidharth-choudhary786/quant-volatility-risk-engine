import numpy as np
import pandas as pd
import os

from regime.volatility_regime import detect_volatility_regime
from regime.regime_rules import regime_position_multiplier


# =====================================================
# REGIME-AWARE PORTFOLIO BACKTEST (FAIL-PROOF)
# =====================================================

def run_portfolio_regime_backtest(
    returns_df,
    portfolio_stocks,
    rolling_window=60
):
    """
    Regime-aware portfolio with automatic fallback
    (NEVER produces empty equity)
    """

    # -----------------------------------
    # STEP 1: Return matrix
    # -----------------------------------
    ret_df = (
        returns_df
        .loc[returns_df["Ticker"].isin(portfolio_stocks)]
        .pivot(index="Date", columns="Ticker", values="log_return")
        .sort_index()
    )

    # -----------------------------------
    # STEP 2: Rolling volatility (lagged)
    # -----------------------------------
    vol_df = (
        ret_df
        .rolling(rolling_window)
        .std()
        .shift(1)
    )

    # -----------------------------------
    # STEP 3: Volatility regime
    # -----------------------------------
    regime_df = vol_df.apply(detect_volatility_regime)

    multiplier_df = regime_df.apply(
        lambda col: col.map(regime_position_multiplier)
    )

    # -----------------------------------
    # STEP 4: Inverse volatility weights
    # -----------------------------------
    vol_df = vol_df.replace(0, np.nan)
    inv_vol = 1 / vol_df

    adj_weights = inv_vol * multiplier_df

    weights = adj_weights.div(
        adj_weights.sum(axis=1),
        axis=0
    )

    # -----------------------------------
    # STEP 5: DAILY FALLBACK LOGIC (KEY FIX)
    # -----------------------------------
    portfolio_returns = []

    for date in ret_df.index:
        returns_today = ret_df.loc[date]
        weights_today = weights.loc[date]

        # valid assets today
        valid = (~returns_today.isna()) & (~weights_today.isna())

        if valid.sum() >= 2:
            # use regime-aware weights
            w = weights_today[valid]
            r = returns_today[valid]
            w = w / w.sum()
            port_ret = (w * r).sum()
        else:
            # 🔥 FALLBACK: equal weight
            r = returns_today.dropna()
            if len(r) == 0:
                continue
            port_ret = r.mean()

        portfolio_returns.append((date, port_ret))

    # -----------------------------------
    # STEP 6: Portfolio series
    # -----------------------------------
    port_ret = pd.Series(
        dict(portfolio_returns)
    ).sort_index()

    # ================================
    # 🔥 RISK-CONSTRAINED ALLOCATOR
    # ================================
    from risk_allocator.apply_allocator import apply_risk_allocator

    portfolio_df = pd.DataFrame({
        "Portfolio_Return": port_ret
    })

    portfolio_df = pd.DataFrame({
        "Portfolio_Return": port_ret
    })

    portfolio_df, risk_summary = apply_risk_allocator(
        portfolio_df,
        portfolio_df["Portfolio_Return"]
    )

    # Final safety clean (extra protection)
    portfolio_df = portfolio_df.dropna()

    # Use adjusted outputs
    port_ret = portfolio_df["Adj_Return"]
    portfolio_equity = portfolio_df["Adj_Equity"]

    return port_ret, portfolio_equity, risk_summary




# =====================================================
# PERFORMANCE METRICS
# =====================================================

def portfolio_metrics(portfolio_returns, portfolio_equity):
    trading_days = 252
    eps = 1e-8

    ann_return = (
        portfolio_equity.iloc[-1]
        ** (trading_days / len(portfolio_equity))
        - 1
    )

    ann_vol = portfolio_returns.std() * np.sqrt(trading_days)
    sharpe = ann_return / (ann_vol + eps)

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
# RUN SCRIPT
# =====================================================

if __name__ == "__main__":

    from scripts.preprocess import load_returns_data

    returns_df = load_returns_data()

    portfolio_stocks = [
        "INFY.NS", "TCS.NS", "RELIANCE.NS", "HDFCBANK.NS",
        "ICICIBANK.NS", "LT.NS", "ITC.NS", "SBIN.NS",
        "AXISBANK.NS", "HINDUNILVR.NS"
    ]

    port_ret, port_eq, risk_summary = run_portfolio_regime_backtest(
        returns_df,
        portfolio_stocks
    )


    metrics = portfolio_metrics(port_ret, port_eq)

    print("\n📊 REGIME-AWARE PORTFOLIO PERFORMANCE\n")
    for k, v in metrics.items():
        print(f"{k:20s}: {v:.4f}")

    os.makedirs("outputs/final", exist_ok=True)

    pd.DataFrame({
        "Portfolio_Return": port_ret,
        "Portfolio_Equity": port_eq
    }).to_csv(
        "outputs/final/portfolio_regime_equity.csv"
    )

    print("\n✅ Regime-aware portfolio results saved → outputs/final/")

    # -----------------------------------
    # SAVE METRICS (MISSING PIECE)
    # -----------------------------------
    metrics_df = pd.DataFrame(
        list(metrics.items()),
        columns=["Metric", "Value"]
    )

    metrics_df.to_csv(
        "outputs/final/portfolio_regime_metrics.csv",
        index=False
    )

    print("📁 Portfolio regime metrics saved → outputs/final/portfolio_regime_metrics.csv")


    # -----------------------------------
    # SAVE RISK ALLOCATOR SUMMARY
    # -----------------------------------
    risk_df = pd.DataFrame(
        list(risk_summary.items()),
        columns=["Metric", "Value"]
    )

    risk_df.to_csv(
        "outputs/final/portfolio_regime_risk_allocator.csv",
        index=False
    )

    print("🛡️ Risk allocator summary saved → outputs/final/portfolio_regime_risk_allocator.csv")
