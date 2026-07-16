from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.isotonic import IsotonicRegression


@dataclass
class DirectionCalibrator:
    """
    Calibrates raw classifier probabilities into a better-behaved probability estimate.
    MVP uses isotonic regression.
    """

    isotonic: IsotonicRegression

    def predict_proba(self, p_raw: np.ndarray) -> np.ndarray:
        p_cal = self.isotonic.predict(p_raw)
        return np.clip(p_cal, 0.0, 1.0)


def fit_isotonic_calibrator(p_raw_cal: np.ndarray, y_cal: np.ndarray) -> DirectionCalibrator:
    iso = IsotonicRegression(out_of_bounds="clip")
    iso.fit(p_raw_cal, y_cal)
    return DirectionCalibrator(isotonic=iso)

