from typing import Optional, Callable

import numpy as np
import pandas as pd

from sktime.forecasting.base import BaseForecaster
from sktime.performance_metrics.forecasting import mean_squared_error


def evaluate_forecaster(
    forecaster: BaseForecaster,
    step_length: int,
    y_test: pd.Series,
    X_test: Optional[pd.DataFrame] = None,
    metric: Optional[
        Callable[[np.ndarray | pd.Series, np.ndarray | pd.Series], float]
    ] = None,
    update_params: bool = False,
) -> tuple[float, pd.Series]:
    """Returns the score of the model on the given metric and its predictions.

    We use the following workflow for forecasting:
        1. Predict `step_length` steps ahead
        2. Observe new data
        3. Update using new data (don't update params necessarily)
        4. Repeat steps 2-4 as often as required

    - The model should be already fitted.
    - Default metric is mean squared error.
    """
    if metric is None:
        metric = mean_squared_error

    total_steps = len(y_test)
    metric_evaluations = []
    predictions = []

    for i in range(0, total_steps, step_length):
        # Adjust the forecast horizon for the last chunk
        end_idx = min(i + step_length, total_steps)
        fh = np.arange(1, end_idx - i + 1)

        y_pred = forecaster.predict(fh, X_test)
        predictions.append(y_pred)

        metric_evaluations.append(
            metric(y_test[i:end_idx], y_pred)
        )

        forecaster.update(
            y_test[i:end_idx],
            X_test,
            update_params=update_params,
        )

    return np.mean(metric_evaluations), pd.concat(predictions, axis=0)
