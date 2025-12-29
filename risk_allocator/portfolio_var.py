import numpy as np

def compute_portfolio_var_es(
    portfolio_returns,
    confidence_level=0.95
):
    """
    Historical portfolio VaR & ES (robust)
    """

    # Safety clean
    returns = np.asarray(portfolio_returns)
    returns = returns[np.isfinite(returns)]

    if len(returns) == 0:
        return 0.0, 0.0

    alpha = 1 - confidence_level

    # Historical VaR
    var = abs(
        np.percentile(returns, alpha * 100)
    )

    # Expected Shortfall
    tail_losses = returns[returns <= -var]

    es = abs(tail_losses.mean()) if len(tail_losses) > 0 else var

    return var, es
