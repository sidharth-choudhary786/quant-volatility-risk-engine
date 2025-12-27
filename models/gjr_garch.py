import numpy as np
from arch import arch_model


def fit_gjr(series):
    model = arch_model(
        series,
        mean="Constant",
        vol="GARCH",
        p=1,
        o=1,
        q=1,
        dist="normal",
        rescale=False
    )
    return model.fit(disp="off")


def extract_gjr_params(result):
    alpha = result.params["alpha[1]"]
    beta  = result.params["beta[1]"]
    gamma = result.params["gamma[1]"]

    persistence = alpha + beta + 0.5 * gamma

    return {
        "omega": result.params["omega"],
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "persistence": persistence,
        "AIC": result.aic,
        "BIC": result.bic
    }
