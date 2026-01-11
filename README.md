# Quant Volatility & Risk Engine  
*A research-grade quantitative system built to study volatility, regime behavior, and portfolio risk under realistic market constraints*

---
## Quick Start

create environment
```bash
/opt/homebrew/bin/python3.11 -m venv venv
source venv/bin/activate
```
install dependencies
```bash
pip install -r requirements.txt
```
run entire project
```bash
python -m run.run_full_pipeline
```

## Research Context

This project was built as a response to a common gap in quantitative finance projects:
many systems demonstrate performance, but very few demonstrate **research discipline**.

The goal here is not to optimize metrics, but to design a system that:
- behaves correctly out-of-sample
- remains interpretable across regimes
- exposes failure modes instead of hiding them

This context informs every design decision in the pipeline.


## Who This Project Is For

- MSc / MTech / PhD students working on quantitative finance projects  
- Candidates preparing for quant research or trading interviews  
- Researchers interested in volatility modeling and regime-aware systems  
- Engineers and students interested in how professional quantitative research pipelines are structured


## Why This Project Matters

Most trading and quant projects focus on maximizing returns using static backtests.
This project focuses on **building a realistic research system** that survives
out-of-sample testing, regime changes, and market stress.

The emphasis is on:
- correctness over curve-fitting  
- robustness over short-term performance  
- transparency over black-box optimization  

This reflects how real quantitative research is conducted in industry.


## What Makes This Project Different

- Fully automated end-to-end pipeline (one command)
- Rolling walk-forward evaluation (no look-ahead bias)
- Explicit regime-aware logic (not hidden ML)
- Portfolio-level risk controls (VaR, ES, stress tests)
- Diagnostics-first mindset (failure analysis, not just returns)

## How This Project Should Be Read

This repository is not meant to be skimmed like a typical trading strategy.

It is structured to show **how decisions are made**, not just what the final metrics are.

If you are reviewing this as:
- a researcher → focus on walk-forward logic and diagnostics
- an interviewer → focus on design decisions and failure analysis
- an engineer → focus on modularity and reproducibility

The results matter, but the **thinking behind the results matters more**.


## Key Design Decisions

Some deliberate choices shaped this system:

- Walk-forward evaluation is used instead of static splits to reflect how models are deployed in practice.
- Regime logic is rule-based and observable, avoiding opaque decision boundaries.
- Risk controls operate at the portfolio level, not as post-processing filters.
- Diagnostics are treated as first-class outputs, not optional analysis.

These decisions trade raw performance for interpretability and robustness.



## 1. What this project is about (in simple words)
The entire research pipeline is fully automated and reproducible.

Instead of focusing on “high returns”, the goal is to build a system that is:

- statistically sound  
- free from look-ahead bias  
- robust across market regimes  
- transparent and diagnosable  
---


## 2. Key ideas implemented

### Volatility modeling
- GARCH, GJR-GARCH, EGARCH, FIGARCH

### Research discipline
- Rolling walk-forward re-fitting  
- Dynamic model selection  
- Strict train → test separation  
- No data leakage  

### Strategy logic
- Volatility targeting  
- Volatility regime detection (LOW / MEDIUM / HIGH)  
- Risk-adjusted signal: Expected Return ÷ Forecasted Volatility  

### Portfolio & risk
- Inverse-volatility weighted portfolios  
- Regime-aware portfolio allocation  
- Portfolio-level VaR & Expected Shortfall constraints  
- Stress testing (COVID-19, rate-hike regimes)  
- Capital allocation checks  

### Diagnostics
- Regime-wise performance attribution  
- Risk allocator behavior analysis  
- Crisis-specific drawdown analysis  
- Visual equity curves for interpretation  


## 3. Project structure (clean & modular)

```
quant-volatility-risk-engine/
│
├── backtest/              # Single asset & portfolio backtests
├── walkforward/           # Rolling walk-forward framework
├── models/                # GARCH family models
├── model_switching/       # Dynamic model selection
├── regime/                # Volatility regime logic
├── risk/                  # VaR, ES, stress testing
├── risk_allocator/        # Risk-constrained scaling
├── strategy/              # Signals & position sizing
├── diagnostics/           # Research diagnostics
├── scripts/               # Data preprocessing & runners
├── run/                   # One-command pipeline runner
├── tests/                 # Sanity checks
├── outputs/
│   ├── final/             # CSV results
│   └── charts/            # All plots
└── README.md
```

---

## 4. Environment setup (clean & reproducible)

### Step 1: Install Python (macOS / Linux)

```bash
brew install python@3.11
/opt/homebrew/bin/python3.11 --version
```

Expected:
```
Python 3.11.x
```

---

### Step 2: Create virtual environment

```bash
/opt/homebrew/bin/python3.11 -m venv venv
source venv/bin/activate
```

> Always use a fresh virtual environment.


---

### Step 3: Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 5. One-command execution (FULL PIPELINE)

Once setup is done, **everything runs with one command**:

```bash
python -m run.run_full_pipeline
```

This single command executes:

1. Data preprocessing  
2. Rolling walk-forward modeling  
3. Walk-forward evaluation + equity plot  
4. Single-asset strategy backtest  
5. Baseline portfolio backtest  
6. Regime-aware portfolio + risk allocator  
7. Portfolio comparison  
8. VaR & Expected Shortfall  
9. Stress testing & capital allocation  
10. Full diagnostics + plots  

No manual steps. No hidden scripts.

---
## 6. Outputs & Artifacts

All outputs are saved under the `outputs/` directory and represent final
research results produced by the pipeline.

### 6.1 Research Tables (CSV)

Location: `outputs/final/`

- walk-forward evaluation metrics  
- single asset performance results  
- baseline portfolio metrics  
- regime-aware portfolio metrics  
- portfolio comparison results  
- VaR and Expected Shortfall summaries  
- stress testing outputs  
- capital allocation results  
- additional diagnostic tables (regime and allocator behavior)

Examples:
- walkforward_metrics.csv
- portfolio_regime_metrics.csv
- portfolio_comparison.csv

### 6.2 Visual Diagnostics (Plots)

Location: `outputs/charts/`

- walk-forward equity curve  
- single asset equity curve  
- baseline vs regime-aware portfolio equity  
- volatility regime distribution  
- crisis-period equity curves (COVID-19, rate hikes)


## 7. Diagnostics philosophy

Most quantitative projects stop at reporting Sharpe ratios.

This project focuses on understanding *behavior* rather than optimizing metrics.
Diagnostics are used to answer practical research questions:

- When does the strategy underperform?
- Which volatility regimes contribute most to drawdowns?
- Does the risk allocator actually activate, and when?
- How does the system behave during real market crises?

These diagnostics follow standard practices used in professional quantitative research.

---

## 8. How Good Are the Results? (Honest Assessment)

The results are reasonable and internally consistent rather than aggressively optimized for in-sample performance.
Performance naturally decreases as evaluation constraints become stricter, which is consistent with robust out-of-sample testing.

At the portfolio level, adding regime awareness improves overall
risk-adjusted behavior, mainly by reducing drawdowns during high
volatility periods. Risk is managed, but not removed, which aligns with
how real trading systems behave.

Overall, the outcomes are believable and reflect realistic performance
for volatility- and regime-based strategies.


## 9. Academic & industry level

This project comfortably sits at:

- **Strong MSc / MTech final project**
- **Early PhD-level research prototype**
- **Quant research internship / analyst portfolio**

It is **far above**:
- Indicator-based trading bots  
- Static backtests  
- ML-for-the-sake-of-ML projects  

---

## 10. Disclaimer

This project reflects my approach to quantitative research:
explicit assumptions, controlled experimentation, and honest evaluation under uncertainty.

---

## 11. Author

Designed and implemented end-to-end as a personal quantitative research system.
This project reflects how I approach quantitative problems:
define assumptions clearly, test them under realistic constraints,
and evaluate results with transparency rather than optimism.

