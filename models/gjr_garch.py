from arch import arch_model
import numpy as np

# -----------------------------------
# Fit GJR-GARCH(1,1)
# -----------------------------------
def fit_gjr_garch(series):
    model = arch_model(
        series,
        mean="Constant",
        vol="GARCH",
        p=1,
        o=1,   # GJR asymmetry term
        q=1,
        dist="normal",
        rescale=False
    )
    return model.fit(disp="off")


# -----------------------------------
# Extract parameters
# -----------------------------------
def extract_gjr_params(gjr_result):
    params = gjr_result.params

    omega = params["omega"]
    alpha = params["alpha[1]"]
    beta  = params["beta[1]"]
    gamma = params["gamma[1]"]

    persistence = alpha + beta + 0.5 * gamma

    return {
        "omega": omega,
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "persistence": persistence,
        "AIC": gjr_result.aic,
        "BIC": gjr_result.bic
    }
