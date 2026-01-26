import pandas as pd

from diagnostics.regime_performance import regime_performance
from diagnostics.allocator_diagnostics import allocator_stats
from diagnostics.crisis_analysis import crisis_window

from backtest.single_asset import run_single_asset_backtest
from models.egarch import fit_egarch
from scripts.preprocess import load_returns_data

from diagnostics.crisis_analysis import plot_crisis_equity

def main():
    print("\n RUNNING FULL DIAGNOSTICS SUITE\n")

    # -----------------------------------
    # Load data & run base backtest
    # -----------------------------------
    returns_df = load_returns_data()

    stock = "INFY.NS"
    series = (
        returns_df
        .loc[returns_df["Ticker"] == stock, "log_return"]
        .dropna()
        .values
    )

    model = fit_egarch(series)

    backtest_df = run_single_asset_backtest(
        returns_df,
        model,
        stock
    )

    # -----------------------------------
    # Diagnostic 1: Regime Performance
    # -----------------------------------
    print(" Diagnostic–1: Regime-wise Performance\n")

    regime_df = regime_performance(backtest_df)
    print(regime_df)

    from diagnostics.regime_performance import plot_regime_distribution
    plot_regime_distribution(backtest_df)


    regime_df.to_csv(
        "outputs/final/diagnostic_regime_performance.csv",
        index=False
    )

    # -----------------------------------
    # Diagnostic 2: Risk Allocator Stats
    # -----------------------------------
    print("\n Diagnostic–2: Risk Allocator Behavior\n")

    allocator_df = pd.read_csv(
        "outputs/final/portfolio_regime_risk_allocator.csv"
    )

    allocator_summary = allocator_stats(allocator_df)
    print(allocator_summary)

    pd.DataFrame(
        allocator_summary.items(),
        columns=["Metric", "Value"]
    ).to_csv(
        "outputs/final/diagnostic_allocator_stats.csv",
        index=False
    )

    # -----------------------------------
    # Diagnostic 3: Crisis Windows
    # -----------------------------------
    print("\n Diagnostic–3: Crisis Stress Test\n")

    crises = [
        ("COVID-19", "2020-02-01", "2020-05-01"),
        ("Rate Hikes", "2022-01-01", "2022-10-01")
    ]

    crisis_results = []

    for name, start, end in crises:
        out = crisis_window(backtest_df, start, end)
        out["Crisis"] = name
        crisis_results.append(out)

        print(f"{name}: {out}")
        plot_crisis_equity(
            backtest_df,
            start,
            end,
            name
        )


    pd.DataFrame(crisis_results).to_csv(
        "outputs/final/diagnostic_crisis_analysis.csv",
        index=False
    )

    print("\n ALL DIAGNOSTICS COMPLETED SUCCESSFULLY")
    print(" Results saved in: outputs/final/\n")


if __name__ == "__main__":
    main()
