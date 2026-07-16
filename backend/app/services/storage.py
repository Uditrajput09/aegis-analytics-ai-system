from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine, select
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.sqlite import insert as sqlite_insert


Base = declarative_base()


class BarORM(Base):
    __tablename__ = "bars"

    symbol = Column(String, primary_key=True)
    timeframe = Column(String, primary_key=True)  # e.g., "1m", "1d"
    ts_utc = Column(DateTime, primary_key=True)

    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=True)


class PredictionORM(Base):
    __tablename__ = "predictions"

    symbol = Column(String, primary_key=True)
    timeframe = Column(String, primary_key=True)
    horizon = Column(String, primary_key=True)  # e.g. "5m", "1d"
    base_ts_utc = Column(DateTime, primary_key=True)

    created_ts_utc = Column(DateTime, nullable=False)

    last_close = Column(Float, nullable=False)
    expected_return = Column(Float, nullable=False)
    expected_price = Column(Float, nullable=False)
    p_up = Column(Float, nullable=True)

    interval_low = Column(Float, nullable=False)
    interval_high = Column(Float, nullable=False)

    model_version = Column(String, nullable=False)
    model_timestamp_utc = Column(DateTime, nullable=False)


def _ensure_parent_dir(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def init_db(db_path: str) -> None:
    _ensure_parent_dir(db_path)
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    engine.dispose()


def _to_utc_naive(dt: pd.Timestamp) -> datetime:
    ts = pd.Timestamp(dt)
    if ts.tzinfo is not None:
        ts = ts.tz_convert("UTC").tz_localize(None)
    return ts.to_pydatetime()


def upsert_bars(db_path: str, symbol: str, timeframe: str, df: pd.DataFrame) -> int:
    """
    Upsert OHLCV bars into SQLite.
    df is expected to have columns: open, high, low, close, volume and a datetime index.
    """
    if df.empty:
        return 0

    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        records = []
        for ts, row in df.iterrows():
            records.append(
                {
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "ts_utc": _to_utc_naive(pd.Timestamp(ts)),
                    "open": float(row["Open"]) if "Open" in row else float(row["open"]),
                    "high": float(row["High"]) if "High" in row else float(row["high"]),
                    "low": float(row["Low"]) if "Low" in row else float(row["low"]),
                    "close": float(row["Close"]) if "Close" in row else float(row["close"]),
                    "volume": None if pd.isna(row.get("Volume", row.get("volume"))) else int(row.get("Volume", row.get("volume"))),
                }
            )

        stmt = sqlite_insert(BarORM).values(records)
        # Update duplicates with newer values (safe for polling).
        update_cols = {c.name: getattr(stmt.excluded, c.name) for c in BarORM.__table__.columns if c.name not in ["symbol", "timeframe", "ts_utc"]}
        stmt = stmt.on_conflict_do_update(
            index_elements=["symbol", "timeframe", "ts_utc"],
            set_=update_cols,
        )
        session.execute(stmt)
        session.commit()

        return len(records)
    finally:
        session.close()
        engine.dispose()


def fetch_bars(db_path: str, symbol: str, timeframe: str, start_utc: Optional[datetime] = None, end_utc: Optional[datetime] = None) -> pd.DataFrame:
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        q = select(BarORM).where(BarORM.symbol == symbol, BarORM.timeframe == timeframe)
        if start_utc is not None:
            q = q.where(BarORM.ts_utc >= start_utc)
        if end_utc is not None:
            q = q.where(BarORM.ts_utc <= end_utc)
        q = q.order_by(BarORM.ts_utc.asc())
        rows = session.execute(q).scalars().all()

        if not rows:
            return pd.DataFrame()

        data = {
            "open": [r.open for r in rows],
            "high": [r.high for r in rows],
            "low": [r.low for r in rows],
            "close": [r.close for r in rows],
            "volume": [r.volume for r in rows],
        }
        index = [r.ts_utc for r in rows]
        df = pd.DataFrame(data, index=pd.to_datetime(index))
        return df
    finally:
        session.close()
        engine.dispose()


def upsert_prediction(
    db_path: str,
    *,
    symbol: str,
    timeframe: str,
    horizon: str,
    base_ts_utc: datetime,
    created_ts_utc: datetime,
    last_close: float,
    expected_return: float,
    expected_price: float,
    p_up: Optional[float],
    interval_low: float,
    interval_high: float,
    model_version: str,
    model_timestamp_utc: datetime,
) -> None:
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        stmt = sqlite_insert(PredictionORM).values(
            symbol=symbol,
            timeframe=timeframe,
            horizon=horizon,
            base_ts_utc=base_ts_utc,
            created_ts_utc=created_ts_utc,
            last_close=last_close,
            expected_return=expected_return,
            expected_price=expected_price,
            p_up=p_up,
            interval_low=interval_low,
            interval_high=interval_high,
            model_version=model_version,
            model_timestamp_utc=model_timestamp_utc,
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["symbol", "timeframe", "horizon", "base_ts_utc"],
            set_={
                "created_ts_utc": stmt.excluded.created_ts_utc,
                "last_close": stmt.excluded.last_close,
                "expected_return": stmt.excluded.expected_return,
                "expected_price": stmt.excluded.expected_price,
                "p_up": stmt.excluded.p_up,
                "interval_low": stmt.excluded.interval_low,
                "interval_high": stmt.excluded.interval_high,
                "model_version": stmt.excluded.model_version,
                "model_timestamp_utc": stmt.excluded.model_timestamp_utc,
            },
        )
        session.execute(stmt)
        session.commit()
    finally:
        session.close()
        engine.dispose()


def fetch_latest_prediction(db_path: str, symbol: str, timeframe: str, horizon: str) -> Optional[PredictionORM]:
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        q = (
            select(PredictionORM)
            .where(
                PredictionORM.symbol == symbol,
                PredictionORM.timeframe == timeframe,
                PredictionORM.horizon == horizon,
            )
            .order_by(PredictionORM.base_ts_utc.desc())
            .limit(1)
        )
        row = session.execute(q).scalars().first()
        return row
    finally:
        session.close()
        engine.dispose()

