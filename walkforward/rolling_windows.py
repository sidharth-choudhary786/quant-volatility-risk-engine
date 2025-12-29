import pandas as pd
from dateutil.relativedelta import relativedelta

def generate_rolling_windows(dates, train_years, test_months):
    """
    Generates rolling (train_start, train_end, test_start, test_end)
    """

    dates = pd.to_datetime(dates).sort_values().unique()

    start_date = dates[0]
    end_date   = dates[-1]

    windows = []

    train_start = start_date

    while True:
        train_end = train_start + relativedelta(years=train_years)
        test_start = train_end
        test_end = test_start + relativedelta(months=test_months)

        if test_end > end_date:
            break

        windows.append(
            (train_start, train_end, test_start, test_end)
        )

        train_start = train_start + relativedelta(months=test_months)

    return windows
