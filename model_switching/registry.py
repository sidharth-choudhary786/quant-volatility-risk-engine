from arch import arch_model

def fit_model(series, model_type):
    """
    Fits a volatility model and returns fitted result.
    """

    if model_type == "GARCH":
        model = arch_model(
            series,
            mean="Constant",
            vol="GARCH",
            p=1, q=1,
            dist="normal",
            rescale=False
        )

    elif model_type == "EGARCH":
        model = arch_model(
            series,
            mean="Constant",
            vol="EGARCH",
            p=1, o=1, q=1,
            dist="normal",
            rescale=False
        )

    elif model_type == "GJR":
        model = arch_model(
            series,
            mean="Constant",
            vol="GARCH",
            p=1, o=1, q=1,
            dist="normal",
            rescale=False
        )

    elif model_type == "FIGARCH":
        model = arch_model(
            series,
            mean="Constant",
            vol="FIGARCH",
            p=1, q=1,
            dist="normal",
            rescale=False
        )

    else:
        raise ValueError("Unknown model type")

    return model.fit(disp="off")
