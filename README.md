# Quant Volatility & Risk Engine  
*A complete, reproducible quantitative research system for volatility modeling, regime-aware strategies, and portfolio risk control*

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

## 1. What this project is about (in simple words)
The entire research pipeline is fully automated and reproducible.

Instead of focusing on “high returns”, the goal is to build a system that is:

- statistically sound  
- free from look-ahead bias  
- robust across market regimes  
- transparent and diagnosable  
---

## 2. Key ideas implemented

The project implements the following ideas end-to-end:

### Volatility modeling
- GARCH
- GJR-GARCH
- EGARCH
- FIGARCH

### Research discipline
- Rolling **walk-forward re-fitting**
- Dynamic model selection
- No data leakage
- Strict train → test separation

### Strategy logic
- Volatility targeting
- Volatility regime detection (LOW / MEDIUM / HIGH)
- Risk-adjusted signal:  
  **Expected Return ÷ Forecasted Volatility**

### Portfolio & risk
- Inverse-volatility weighted portfolios
- Regime-aware portfolio allocation
- Portfolio-level **VaR & Expected Shortfall constraints**
- Stress testing (COVID-19, rate-hike regimes)
- Capital allocation checks

### Diagnostics (what most projects miss)
- Regime-wise performance attribution
- Risk allocator behavior analysis
- Crisis-specific drawdown analysis
- Visual equity curves for interpretation

---

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


## 7. Diagnostics philosophy (why this matters)

Most projects stop at Sharpe ratios.

This project answers deeper questions:

- When does the strategy fail?
- Which regimes contribute most to drawdowns?
- Does risk control actually activate?
- How does the system behave in real crises?

These diagnostics align with standard practices used in professional quantitative research.


## How to Interpret the Results

- Walk-forward equity confirms the absence of look-ahead bias.
- Regime-aware portfolio sacrifices some return to reduce tail risk.
- Risk allocator remains inactive in normal conditions and activates only during stress.
- Crisis plots demonstrate realistic drawdowns rather than artificial smooth curves.

These behaviors are expected and desired in institutional-grade systems.

---

## 8. How Good Are the Results? (Honest Assessment)

The results are reasonable and internally consistent rather than
exceptional. Performance naturally decreases as evaluation constraints become stricter, which is consistent with robust out-of-sample testing.

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

This project is strictly for **research and educational purposes**.  
It is not financial advice and not a live trading system.

---

## 11. Author

Designed and implemented independently as a full quantitative research system,
with emphasis on statistical rigor, realistic assumptions,
and professional research practices.
