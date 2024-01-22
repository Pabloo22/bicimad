from typing import Optional

import numpy as np
import pandas as pd

from sktime.forecasting.base import BaseForecaster


def get_rolling_predictions(
    forecaster: BaseForecaster,
    step_length: int,
    y_test: pd.Series,
    X_test: Optional[pd.DataFrame] = None,
    update_params: bool = False,
) -> pd.Series:
    """Returns the predictions of the model.

    We use the following workflow for forecasting:
        1. Predict `step_length` steps ahead
        2. Observe new data
        3. Update using new data (don't update params necessarily)
        4. Repeat steps 2-4 as often as required

    Note: The model should be already fitted.
    """
    total_steps = len(y_test)
    predictions = []

    for i in range(0, total_steps, step_length):
        # Adjust the forecast horizon for the last chunk
        end_idx = min(i + step_length, total_steps)

        length_out = end_idx - i
        if length_out < 3:
            # We need at least 3 steps to make a prediction
            break

        sliced_y = y_test[i:end_idx]
        sliced_X = X_test[i:end_idx] if X_test is not None else None
        y_pred = forecaster.update_predict(
            sliced_y,
            X=sliced_X,
            update_params=update_params,
            reset_forecaster=False,
        )
        predictions.append(y_pred)

    return pd.concat(predictions, axis=0)
