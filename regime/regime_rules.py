def regime_position_multiplier(regime):
    """
    Position control based on volatility regime
    """

    if regime == "LOW":
        return 1.2     # slightly aggressive
    elif regime == "MEDIUM":
        return 1.0     # normal
    elif regime == "HIGH":
        return 0.5     # defensive
    else:
        return 0.0     # UNKNOWN → no trade
