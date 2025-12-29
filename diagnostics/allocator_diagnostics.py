def allocator_stats(risk_summary_df):
    """
    Diagnostics for risk allocator behavior
    """

    # Convert key-value CSV → dictionary
    summary = dict(
        zip(risk_summary_df["Metric"], risk_summary_df["Value"])
    )

    scale = summary["Risk_Scale"]
    var = summary["Portfolio_VaR"]
    es = summary["Portfolio_ES"]

    return {
        "Risk_Scale": scale,
        "Portfolio_VaR": var,
        "Portfolio_ES": es,
        "Allocator_Active": scale < 1.0
    }
