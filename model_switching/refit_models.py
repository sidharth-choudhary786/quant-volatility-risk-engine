import pandas as pd
from model_switching.registry import fit_model

MODELS = ["GARCH", "EGARCH", "GJR", "FIGARCH"]

def refit_all_models(series):
    """
    Fits all models and returns AIC/BIC + stability metrics.
    """

    results = []

    for model_name in MODELS:
        try:
            res = fit_model(series, model_name)

            # Stability filter
            persistence = None
            if "alpha[1]" in res.params and "beta[1]" in res.params:
                persistence = res.params["alpha[1]"] + res.params["beta[1]"]

            results.append({
                "Model": model_name,
                "AIC": res.aic,
                "BIC": res.bic,
                "Persistence": persistence,
                "Result": res
            })

        except Exception:
            continue

    return pd.DataFrame(results)
