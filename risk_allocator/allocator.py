import numpy as np
from risk_allocator.config import (
    MAX_PORTFOLIO_VAR,
    MAX_PORTFOLIO_ES,
    MIN_SCALE,
    MAX_SCALE
)
from risk_allocator.portfolio_var import compute_portfolio_var_es

def risk_constrained_scaler(portfolio_returns):
    """
    Returns scaling factor based on portfolio risk
    """

    var, es = compute_portfolio_var_es(portfolio_returns)

    # Safety fallback
    if var <= 0 or es <= 0:
        return MAX_SCALE, var, es

    var_ratio = MAX_PORTFOLIO_VAR / var
    es_ratio  = MAX_PORTFOLIO_ES  / es

    scale = min(var_ratio, es_ratio)

    # Clip to safety bounds
    scale = np.clip(scale, MIN_SCALE, MAX_SCALE)

    return scale, var, es
