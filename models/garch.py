from arch import arch_model
import numpy as np

# -----------------------------------
# Fit GARCH(1,1)
# -----------------------------------
def fit_garch(series):
    model = arch_model(
        series,
        mean="Constant",
        vol="GARCH",
        p=1,
        q=1,
        dist="normal",
        rescale=False
    )
    return model.fit(disp="off")


# -----------------------------------
# Extract parameters
# -----------------------------------
def extract_garch_params(garch_result):
    params = garch_result.params

    alpha = params["alpha[1]"]
    beta  = params["beta[1]"]
    omega = params["omega"]

    persistence = alpha + beta
    long_run_vol = np.sqrt(omega / (1 - persistence))

    return {
        "omega": omega,
        "alpha": alpha,
        "beta": beta,
        "persistence": persistence,
        "long_run_vol": long_run_vol,
        "AIC": garch_result.aic,
        "BIC": garch_result.bic
    }
