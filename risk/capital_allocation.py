import pandas as pd
import numpy as np

# -------------------------------------------------
# CAPITAL ALLOCATION & ADEQUACY CHECK
# -------------------------------------------------

def _to_float(x):
    """
    Safely convert scalar / pandas / numpy values to float
    WITHOUT changing numerical meaning.
    """
    if isinstance(x, (pd.Series, pd.DataFrame)):
        x = x.values.flatten()[0]
    return float(x)

def capital_allocation_analysis(
    var_95,
    es_95,
    stress_5d,
    available_capital=0.30
):
    """
    Capital adequacy decision using:
    - VaR
    - Expected Shortfall
    - Stress losses

    Logic EXACTLY SAME as Code 15
    """

    # -------- SAFE CAST (pipeline proof) --------
    var_95 = _to_float(var_95)
    es_95 = _to_float(es_95)
    stress_5d = _to_float(stress_5d)
    available_capital = _to_float(available_capital)

    # -------- Capital requirement --------
    capital_required = max(es_95, stress_5d)

    risk_status = (
        "SAFE"
        if available_capital >= capital_required
        else "UNDER-CAPITALIZED"
    )

    # -------- Summary table --------
    capital_summary = pd.DataFrame({
        "Metric": [
            "VaR (95%)",
            "Expected Shortfall (95%)",
            "Stress Loss (5-Day)",
            "Capital Required",
            "Available Capital",
            "Risk Status"
        ],
        "Value": [
            f"{var_95 * 100:.2f}%",
            f"{es_95 * 100:.2f}%",
            f"{stress_5d * 100:.2f}%",
            f"{capital_required * 100:.2f}%",
            f"{available_capital * 100:.2f}%",
            risk_status
        ]
    })

    return capital_summary
