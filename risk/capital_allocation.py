import pandas as pd

# -------------------------------------------------
# CAPITAL ALLOCATION & ADEQUACY ANALYSIS
# -------------------------------------------------

def run_capital_allocation_analysis(
    garch_var,
    es_df,
    garch_stress_loss,
    multi_day_stress_loss,
    available_capital=0.30
):
    """
    Capital requirement & adequacy analysis.

    Logic EXACTLY SAME as Code 15.
    No change in formulas or decisions.
    """

    # -----------------------------------
    # Collect key risk measures
    # -----------------------------------

    # VaR (95%)
    var_95 = abs(garch_var.mean())

    # Expected Shortfall (95%)
    es_95 = abs(es_df["GARCH_ES"].mean())

    # Stress losses
    stress_1d = garch_stress_loss
    stress_5d = multi_day_stress_loss

    # -----------------------------------
    # Risk comparison table
    # -----------------------------------
    risk_table = pd.DataFrame({
        "Risk Measure": [
            "VaR (95%)",
            "Expected Shortfall (95%)",
            "Stress Loss (1-Day)",
            "Stress Loss (5-Day)"
        ],
        "Estimated Loss (%)": [
            var_95 * 100,
            es_95 * 100,
            stress_1d * 100,
            stress_5d * 100
        ]
    })

    # -----------------------------------
    # Capital requirement logic
    # -----------------------------------
    capital_requirement = max(es_95, stress_5d)

    # Capital adequacy decision
    if available_capital >= capital_requirement:
        risk_status = "SAFE"
    else:
        risk_status = "UNDER-CAPITALIZED"

    # -----------------------------------
    # Final capital summary
    # -----------------------------------
    final_risk_summary = pd.DataFrame({
        "Metric": [
            "VaR (95%)",
            "Expected Shortfall (95%)",
            "Stress Loss (5-Day)",
            "Capital Required",
            "Available Capital",
            "Risk Status"
        ],
        "Value": [
            f"{var_95*100:.2f}%",
            f"{es_95*100:.2f}%",
            f"{stress_5d*100:.2f}%",
            f"{capital_requirement*100:.2f}%",
            f"{available_capital*100:.2f}%",
            risk_status
        ]
    })

    return {
        "Risk_Table": risk_table,
        "Capital_Required": capital_requirement,
        "Available_Capital": available_capital,
        "Risk_Status": risk_status,
        "Final_Summary": final_risk_summary
    }

