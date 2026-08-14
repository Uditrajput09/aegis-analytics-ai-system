from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

import pandas as pd
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

from backend.app.core.types import Bar, BarsResponse, PredictionLatest, RiskLatest
from backend.app.features.feature_builder import Timeframe
from backend.app.services.predictor import get_latest_prediction_or_none, predict_latest
from backend.app.services.storage import fetch_bars, upsert_bars
from backend.app.services.yahoo_client import fetch_ohlcv

router = APIRouter()
_HORIZON_RE = re.compile(r"^(\d+)([md])$")
_MODEL_FILE_RE = re.compile(r"^(.+)_(1m|1d)_(\d+[md])_(.+)\.joblib$")


def _predict_latest_http(
    *,
    symbol: str,
    timeframe: Timeframe,
    horizon: str,
    model_version: str = "mvp_v1",
    db_path: str,
):
    """Run inference; map predictable failures to HTTP errors instead of raw 500s."""
    try:
        return predict_latest(
            symbol=symbol,
            timeframe=timeframe,
            horizon=horizon,
            model_version=model_version,
            db_path=db_path,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


def _normalize_horizon_or_400(horizon: str) -> str:
    h = horizon.lower().strip()
    match = _HORIZON_RE.match(h)
    if not match:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid horizon: {horizon}. Use formats like 5m, 15m, 60m, or 1d.",
        )
    return f"{int(match.group(1))}{match.group(2)}"


def _normalize_timeframe_or_400(timeframe: str) -> Timeframe:
    tf = timeframe.lower().strip()
    if tf not in {"1m", "1d"}:
        raise HTTPException(status_code=400, detail=f"Unsupported timeframe: {timeframe}. Use '1m' or '1d'.")
    return tf  # type: ignore[return-value]


def _infer_timeframe_from_horizon(horizon: str) -> Timeframe:
    h = _normalize_horizon_or_400(horizon)
    return "1m" if h.endswith("m") else "1d"


@router.get("/health")
def health():
    return {"ok": True, "time_utc": datetime.now(timezone.utc).isoformat()}


def _trained_symbols(model_dir: str) -> List[str]:
    symbols: set[str] = set()
    for path in Path(model_dir).glob("*.joblib"):
        match = _MODEL_FILE_RE.match(path.name)
        if match:
            symbols.add(match.group(1).replace("_", "/"))
    return sorted(symbols)


@router.get("/meta/symbols")
def meta_symbols():
    """Symbols that have at least one trained model artifact on disk."""
    from backend.app.core.config import load_settings

    settings = load_settings()
    return {"symbols": _trained_symbols(settings.model_dir)}


@router.get("/")
def root():
    return {
        "name": "Aegis Analytics AI API",
        "status": "ok",
        "docs": "/docs",
        "routes": ["/health", "/meta/symbols", "/bars/recent", "/predictions/latest", "/risk/latest"],
    }


@router.get("/favicon.ico", include_in_schema=False)
def favicon():
    # Avoid noisy browser 404 logs for favicon requests.
    return Response(status_code=204)


@router.get("/bars/recent", response_model=BarsResponse)
def bars_recent(
    symbol: str = Query(..., description="Ticker symbol, e.g. AAPL"),
    timeframe: str = Query("1m", description="Bar timeframe: 1m or 1d"),
    limit: int = Query(300, ge=10, le=5000),
):
    from backend.app.core.config import load_settings

    settings = load_settings()
    timeframe = _normalize_timeframe_or_400(timeframe)
    df = fetch_bars(settings.data_db_path, symbol=symbol.upper(), timeframe=timeframe)
    if df.empty:
        # On-demand fetch if DB is empty.
        interval = "1m" if timeframe == "1m" else "1d"
        period = f"{settings.intraday_lookback_days}d" if timeframe == "1m" else "1y"
        ydf = fetch_ohlcv(symbol.upper(), interval=interval, period=period)
        if ydf.empty:
            raise HTTPException(status_code=404, detail="No data from Yahoo Finance")
        upsert_bars(settings.data_db_path, symbol=symbol.upper(), timeframe=timeframe, df=ydf)
        df = fetch_bars(settings.data_db_path, symbol=symbol.upper(), timeframe=timeframe)

    df = df.tail(limit)
    bars = [
        Bar(
            symbol=symbol.upper(),
            timeframe=timeframe,
            ts_utc=ts.to_pydatetime() if hasattr(ts, "to_pydatetime") else ts,
            open=float(r["open"]),
            high=float(r["high"]),
            low=float(r["low"]),
            close=float(r["close"]),
            volume=None if pd.isna(r.get("volume")) else int(r.get("volume")),
        )
        for ts, r in df.iterrows()
    ]
    return BarsResponse(symbol=symbol.upper(), timeframe=timeframe, bars=bars)


@router.get("/predictions/latest", response_model=PredictionLatest)
def predictions_latest(
    symbol: str = Query(...),
    horizon: str = Query(..., description="e.g. 5m, 15m, 60m, 1d"),
    timeframe: Optional[str] = Query(None, description="If omitted, inferred from horizon"),
    force_update: bool = Query(False, description="Compute a new prediction even if cached"),
):
    from backend.app.core.config import load_settings
    settings = load_settings()
    symbol = symbol.upper()
    horizon = _normalize_horizon_or_400(horizon)
    inferred_tf = _infer_timeframe_from_horizon(horizon)
    tf = _normalize_timeframe_or_400(timeframe) if timeframe else inferred_tf
    if tf != inferred_tf:
        raise HTTPException(
            status_code=400,
            detail=f"timeframe '{tf}' does not match horizon '{horizon}'. Expected timeframe '{inferred_tf}'.",
        )

    if not force_update:
        existing = get_latest_prediction_or_none(symbol=symbol, timeframe=tf, horizon=horizon)
        if existing is not None:
            return PredictionLatest(
                symbol=existing.symbol,
                horizon=existing.horizon,
                timeframe=existing.timeframe,
                ts_utc=existing.ts_utc,
                last_close=existing.last_close,
                expected_return=existing.expected_return,
                expected_price=existing.expected_price,
                p_up=existing.p_up,
                interval_low=existing.interval_low,
                interval_high=existing.interval_high,
                model_version=existing.model_version,
                model_timestamp_utc=existing.model_timestamp_utc,
            )

    pred = _predict_latest_http(
        symbol=symbol,
        timeframe=tf,
        horizon=horizon,
        model_version="mvp_v1",
        db_path=settings.data_db_path,
    )
    return PredictionLatest(
        symbol=pred.symbol,
        horizon=pred.horizon,
        timeframe=pred.timeframe,
        ts_utc=pred.ts_utc,
        last_close=pred.last_close,
        expected_return=pred.expected_return,
        expected_price=pred.expected_price,
        p_up=pred.p_up,
        interval_low=pred.interval_low,
        interval_high=pred.interval_high,
        model_version=pred.model_version,
        model_timestamp_utc=pred.model_timestamp_utc,
    )


@router.get("/risk/latest", response_model=RiskLatest)
def risk_latest(
    symbol: str = Query(...),
    horizon: str = Query(...),
    timeframe: Optional[str] = Query(None),
    force_update: bool = Query(False),
):
    from backend.app.core.config import load_settings
    from backend.app.risk.risk_engine import risk_from_interval

    settings = load_settings()
    symbol = symbol.upper()
    horizon = _normalize_horizon_or_400(horizon)
    inferred_tf = _infer_timeframe_from_horizon(horizon)
    tf = _normalize_timeframe_or_400(timeframe) if timeframe else inferred_tf
    if tf != inferred_tf:
        raise HTTPException(
            status_code=400,
            detail=f"timeframe '{tf}' does not match horizon '{horizon}'. Expected timeframe '{inferred_tf}'.",
        )

    pred = get_latest_prediction_or_none(symbol=symbol, timeframe=tf, horizon=horizon)
    if pred is None or force_update:
        pred = _predict_latest_http(
            symbol=symbol,
            timeframe=tf,
            horizon=horizon,
            model_version="mvp_v1",
            db_path=settings.data_db_path,
        )

    risk = risk_from_interval(interval_low=pred.interval_low, interval_high=pred.interval_high)
    return RiskLatest(
        symbol=pred.symbol,
        horizon=pred.horizon,
        timeframe=pred.timeframe,
        ts_utc=pred.ts_utc,
        expected_return=pred.expected_return,
        interval_low=pred.interval_low,
        interval_high=pred.interval_high,
        p_return_below_minus_1pct=risk.p_return_below_minus_1pct,
        p_return_below_minus_2pct=risk.p_return_below_minus_2pct,
    )


from pydantic import BaseModel


class AuthRequest(BaseModel):
    username: str
    password: str


@router.post("/auth/login")
def auth_login(req: AuthRequest):
    from dashboard.user_store import authenticate_user, init_user_store, get_or_create_demo_user

    init_user_store()
    get_or_create_demo_user()
    user = authenticate_user(req.username, req.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    return {
        "ok": True,
        "user": user,
        "token": f"aegis_token_{user['id']}_{int(datetime.now(timezone.utc).timestamp())}",
    }


@router.post("/auth/register")
def auth_register(req: AuthRequest):
    from dashboard.user_store import register_user, init_user_store

    init_user_store()
    ok, msg = register_user(req.username, req.password)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    return {"ok": True, "message": msg}


