
import numpy as np
from arch import arch_model
from statsmodels.stats.diagnostic import het_arch


def fit_garch(series):
    """
    Fit GARCH(1,1) on a univariate return series
    """

    model = arch_model(
        series,
        mean="Constant",
        vol="GARCH",
        p=1,
        q=1,
        dist="normal",
        rescale=False
    )

    result = model.fit(disp="off")
    return result


def garch_diagnostics(garch_result):
    """
    ARCH test on standardized residuals
    """

    std_resid = garch_result.std_resid
    lm_stat, lm_pvalue, _, _ = het_arch(std_resid, nlags=5)

    return {
        "LM_Statistic": lm_stat,
        "LM_pvalue": lm_pvalue
    }


def garch_forecast(garch_result, horizon=5):
    """
    Volatility forecast from fitted GARCH
    """

    forecast = garch_result.forecast(horizon=horizon)
    var_forecast = forecast.variance.values[-1]
    vol_forecast = np.sqrt(var_forecast)

    return vol_forecast


def garch_long_run_vol(garch_result):
    """
    Long-run (unconditional) volatility
    """

    omega = garch_result.params["omega"]
    alpha = garch_result.params["alpha[1]"]
    beta  = garch_result.params["beta[1]"]

    return np.sqrt(omega / (1 - alpha - beta))
