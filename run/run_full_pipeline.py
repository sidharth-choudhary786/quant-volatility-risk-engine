# =========================================================
# FULL PIPELINE RUNNER (MASTER)
# One command → COMPLETE PROJECT EXECUTION
# =========================================================

import os
import pandas as pd
import subprocess

# =========================================================
# CONFIG
# =========================================================

STOCK = "INFY.NS"

PORTFOLIO_STOCKS = [
    "INFY.NS", "TCS.NS", "RELIANCE.NS", "HDFCBANK.NS",
    "ICICIBANK.NS", "LT.NS", "ITC.NS", "SBIN.NS",
    "AXISBANK.NS", "HINDUNILVR.NS"
]

OUTPUT_DIR = "outputs/final"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# SAFE COMMAND RUNNER
# =========================================================

def run_cmd(cmd, title):
    print("\n" + "="*60)
    print(f"▶ {title}")
    print("="*60)
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"FAILED: {title}")
    print(f"✅ DONE: {title}")

# =========================================================
# PIPELINE START
# =========================================================

def main():

    print("\n🚀 STARTING FULL QUANT PIPELINE (ONE COMMAND MODE)\n")

    # -----------------------------------------------------
    # 1️⃣ DATA PREPROCESSING
    # -----------------------------------------------------
    run_cmd(
        "python -m scripts.preprocess",
        "Data preprocessing"
    )

    # -----------------------------------------------------
    # 2️⃣ WALK-FORWARD + MODEL SWITCHING
    # -----------------------------------------------------
    run_cmd(
        "python -m walkforward.run_walkforward",
        "Rolling walk-forward & model re-fitting"
    )

    run_cmd(
        "python -m walkforward.evaluation",
        "Walk-forward evaluation"
    )

    # -----------------------------------------------------
    # 3️⃣ SINGLE ASSET STRATEGY
    # -----------------------------------------------------
    run_cmd(
        "python -m backtest.single_asset",
        "Single asset backtest (regime + return/vol)"
    )

    # -----------------------------------------------------
    # 4️⃣ PORTFOLIO (BASELINE)
    # -----------------------------------------------------
    run_cmd(
        "python -m backtest.portfolio",
        "Baseline portfolio backtest"
    )


    # -----------------------------------------------------
    # 5️⃣ PORTFOLIO (REGIME + RISK ALLOCATOR)
    # -----------------------------------------------------
    run_cmd(
        "python -m backtest.portfolio_regime",
        "Regime-aware portfolio + risk allocator"
    )

    # -----------------------------------------------------
    # 6️⃣ PORTFOLIO COMPARISON
    # -----------------------------------------------------
    run_cmd(
        "python -m backtest.portfolio_compare",
        "Baseline vs Regime portfolio comparison"
    )

    # -----------------------------------------------------
    # 7️⃣ RISK MODULES (SINGLE ASSET)
    # -----------------------------------------------------
    run_cmd(
        "python -m risk.var",
        "Value-at-Risk (VaR)"
    )

    run_cmd(
        "python -m risk.es",
        "Expected Shortfall (ES)"
    )

    run_cmd(
        "python -m risk.stress_testing",
        "Stress testing"
    )

    run_cmd(
        "python -m risk.capital_allocation",
        "Capital allocation check"
    )

    # -----------------------------------------------------
    # 8️⃣ DIAGNOSTICS
    # -----------------------------------------------------
    run_cmd(
        "python -m diagnostics.run_all",
        "Full diagnostics suite"
    )

    print("\n🎉 FULL PIPELINE COMPLETED SUCCESSFULLY")
    print(f"📂 All results saved in → {OUTPUT_DIR}\n")

# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()
