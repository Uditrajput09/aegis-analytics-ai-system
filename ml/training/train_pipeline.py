from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Literal, Tuple

import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier, LGBMRegressor

from backend.app.features.feature_builder import Timeframe, build_features_and_targets, build_latest_features
from ml.confidence.calibration import fit_isotonic_calibrator
from ml.confidence.conformal_intervals import fit_conformal_abs_residuals


@dataclass(frozen=True)
class TrainedArtifact:
    timeframe: str
    horizon: str
    model_version: str
    trained_at_utc: datetime
    feature_columns: List[str]
    regress: LGBMRegressor
    direction: LGBMClassifier
    calibrator: object  # DirectionCalibrator
    conformal: object   # ConformalRegressor

    def to_dict(self) -> dict:
        return {
            "timeframe": self.timeframe,
            "horizon": self.horizon,
            "model_version": self.model_version,
            "trained_at_utc": self.trained_at_utc,
            "feature_columns": self.feature_columns,
            "regress": self.regress,
            "direction": self.direction,
            "calibrator": self.calibrator,
            "conformal": self.conformal,
        }


def _fit_time_splits(X: pd.DataFrame, y_ret: pd.Series, y_up: pd.Series, *, train_frac: float = 0.7, calib_frac: float = 0.15):
    n = len(X)
    if n < 200:
        raise ValueError(f"Not enough rows to train reliably: n={n}")
    train_end = int(n * train_frac)
    calib_end = train_end + int(n * calib_frac)
    if calib_end <= train_end + 10:
        raise ValueError("Calibration split too small")

    X_train = X.iloc[:train_end]
    y_ret_train = y_ret.iloc[:train_end]
    y_up_train = y_up.iloc[:train_end]

    X_cal = X.iloc[train_end:calib_end]
    y_ret_cal = y_ret.iloc[train_end:calib_end]
    y_up_cal = y_up.iloc[train_end:calib_end]
    return X_train, y_ret_train, y_up_train, X_cal, y_ret_cal, y_up_cal


def train_symbol_horizon(
    *,
    symbol: str,
    timeframe: Timeframe,
    horizon: str,
    bars: pd.DataFrame,
    model_dir: str,
    model_version: str = "mvp_v1",
    conformal_alpha: float = 0.1,
    use_gpu: bool = False,
    gpu_platform_id: int = 1,
    gpu_device_id: int = 0,
) -> str:
    X, y_ret, y_up = build_features_and_targets(bars, timeframe=timeframe, horizon=horizon)
    if X.empty:
        raise ValueError(f"No training rows for {symbol} {timeframe} {horizon}")

    X_train, y_ret_train, y_up_train, X_cal, y_ret_cal, y_up_cal = _fit_time_splits(X, y_ret, y_up)

    gpu_kwargs = {}
    if use_gpu:
        gpu_kwargs = {
            "device": "gpu",
            "gpu_platform_id": gpu_platform_id,
            "gpu_device_id": gpu_device_id,
        }

    # Regression: predict return
    reg = LGBMRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=-1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        **gpu_kwargs,
    )
    try:
        reg.fit(X_train, y_ret_train)
    except Exception as e:
        if use_gpu:
            print(f"[train] GPU regressor fit warning/failed ({e}), falling back to CPU...")
            reg = LGBMRegressor(
                n_estimators=300,
                learning_rate=0.05,
                max_depth=-1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
            )
            reg.fit(X_train, y_ret_train)
        else:
            raise

    # Direction: predict up/down
    clf = LGBMClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=-1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        **gpu_kwargs,
    )
    try:
        clf.fit(X_train, y_up_train)
    except Exception as e:
        if use_gpu:
            print(f"[train] GPU classifier fit warning/failed ({e}), falling back to CPU...")
            clf = LGBMClassifier(
                n_estimators=300,
                learning_rate=0.05,
                max_depth=-1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
            )
            clf.fit(X_train, y_up_train)
        else:
            raise

    # Fit calibration for direction probabilities
    p_raw_cal = clf.predict_proba(X_cal)[:, 1]
    calibrator = fit_isotonic_calibrator(p_raw_cal, y_up_cal.values)

    # Fit conformal interval for regression outputs
    y_pred_cal = reg.predict(X_cal)
    conformal = fit_conformal_abs_residuals(y_pred_cal=y_pred_cal, y_cal=y_ret_cal.values, alpha=conformal_alpha)

    artifact = TrainedArtifact(
        timeframe=timeframe,
        horizon=horizon,
        model_version=model_version,
        trained_at_utc=datetime.now(timezone.utc),
        feature_columns=list(X.columns),
        regress=reg,
        direction=clf,
        calibrator=calibrator,
        conformal=conformal,
    )

    Path(model_dir).mkdir(parents=True, exist_ok=True)
    safe_symbol = symbol.replace("/", "_")
    artifact_path = str(Path(model_dir) / f"{safe_symbol}_{timeframe}_{horizon}_{model_version}.joblib")
    joblib.dump(artifact.to_dict(), artifact_path)
    return artifact_path

