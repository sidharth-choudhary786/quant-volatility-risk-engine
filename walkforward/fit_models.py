from arch import arch_model
import numpy as np

def fit_egarch(series):
    """
    EGARCH(1,1) — SAME as existing logic
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

    result = model.fit(disp="off")
    return result
