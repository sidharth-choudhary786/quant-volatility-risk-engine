from arch import arch_model


def fit_figarch(series):
    model = arch_model(
        series,
        mean="Constant",
        vol="FIGARCH",
        p=1,
        q=1,
        dist="normal",
        rescale=False
    )
    return model.fit(disp="off")


def extract_figarch_params(result):
    return {
        "d_parameter": result.params["d"],
        "AIC": result.aic,
        "BIC": result.bic
    }
