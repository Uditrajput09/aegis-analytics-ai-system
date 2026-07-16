from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ConformalRegressor:
    """
    Conformal prediction interval wrapper for regression using absolute residuals.
    Produces symmetric intervals around point predictions.
    """

    residual_q: float

    def predict_interval(self, y_pred: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        q = float(self.residual_q)
        low = y_pred - q
        high = y_pred + q
        return low, high


def fit_conformal_abs_residuals(y_pred_cal: np.ndarray, y_cal: np.ndarray, *, alpha: float) -> ConformalRegressor:
    residuals = np.abs(y_cal - y_pred_cal)
    # Quantile for (1-alpha) coverage. Small-sample correction omitted for MVP simplicity.
    residual_q = float(np.quantile(residuals, 1.0 - alpha))
    return ConformalRegressor(residual_q=residual_q)

