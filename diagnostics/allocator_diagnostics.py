def allocator_stats(risk_summary_df):
    """
    Diagnostics for risk allocator behavior
    (type-safe, confidence-level agnostic)
    """

    # Convert key-value CSV → dictionary
    summary = dict(
        zip(risk_summary_df["Metric"], risk_summary_df["Value"])
    )

    # ---- Robust key detection ----
    var_key = next(k for k in summary if k.startswith("Portfolio_VaR"))
    es_key  = next(k for k in summary if k.startswith("Portfolio_ES"))

    # ---- TYPE FIX (CRITICAL) ----
    scale = float(summary["Risk_Scale"])
    var = float(summary[var_key])
    es = float(summary[es_key])

    return {
        "Risk_Scale": scale,
        var_key: var,
        es_key: es,
        "Allocator_Active": scale < 1.0
    }
