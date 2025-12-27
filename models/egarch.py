import numpy as np
from arch import arch_model


def fit_egarch(series):
    """
    Fit EGARCH(1,1) model on return series
    """
    model = arch_model(
        series,
        mean="Constant",
        vol="EGARCH",
        p=1,
        o=1,
        q=1,
        dist="normal",
        rescale=False
    )
    return model.fit(disp="off")


def extract_egarch_params(result):
    """
    Extract EGARCH parameters safely
    """
    return {
        "omega": result.params["omega"],
        "alpha": result.params["alpha[1]"],
        "beta":  result.params["beta[1]"],
        "gamma": result.params["gamma[1]"],
        "persistence": result.params["alpha[1]"] + result.params["beta[1]"],
        "AIC": result.aic,
        "BIC": result.bic
    }
