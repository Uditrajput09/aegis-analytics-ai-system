from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List


def _split_symbols(value: str) -> List[str]:
    return [s.strip().upper() for s in value.split(",") if s.strip()]


@dataclass(frozen=True)
class Settings:
    symbols: List[str]
    data_db_path: str
    model_dir: str

    intraday_interval: str
    intraday_lookback_days: int
    intraday_horizons_minutes: List[int]

    daily_horizon_days: int

    prediction_refresh_minutes: int

    conformal_alpha: float


def load_settings() -> Settings:
    return Settings(
        symbols=_split_symbols(os.getenv("SYMBOLS", "AAPL,MSFT,GOOGL")),
        data_db_path=os.getenv("DATA_DB_PATH", "data/app.db"),
        model_dir=os.getenv("MODEL_DIR", "models"),
        intraday_interval=os.getenv("INTRADAY_INTERVAL", "1m"),
        intraday_lookback_days=int(os.getenv("INTRADAY_LOOKBACK_DAYS", "7")),
        intraday_horizons_minutes=[5, 15, 60],
        daily_horizon_days=int(os.getenv("DAILY_HORIZON_DAYS", "1")),
        prediction_refresh_minutes=int(os.getenv("PREDICTION_REFRESH_MINUTES", "5")),
        conformal_alpha=float(os.getenv("CONFORMAL_ALPHA", "0.1")),
    )

