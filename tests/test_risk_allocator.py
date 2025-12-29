import numpy as np
import pandas as pd

from risk_allocator.apply_allocator import apply_risk_allocator

def test_risk_allocator_basic():
    """
    Sanity test for risk-constrained portfolio allocator
    """

    np.random.seed(42)

    # Synthetic portfolio returns
    returns = np.random.normal(
        loc=0.0005,
        scale=0.01,
        size=1000
    )

    portfolio_df = pd.DataFrame({
        "Portfolio_Return": returns
    })

    df_out, risk_summary = apply_risk_allocator(
        portfolio_df,
        portfolio_df["Portfolio_Return"]
    )

    # -----------------------
    # Assertions (CRITICAL)
    # -----------------------
    assert "Adj_Return" in df_out.columns
    assert "Risk_Scale" in df_out.columns

    assert 0.3 <= risk_summary["Risk_Scale"] <= 1.0
    assert risk_summary["Portfolio_VaR"] > 0
    assert risk_summary["Portfolio_ES"] > 0

    print("\n✅ Risk allocator test PASSED")
    print(risk_summary)


if __name__ == "__main__":
    test_risk_allocator_basic()
