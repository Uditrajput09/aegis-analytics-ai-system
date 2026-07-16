from __future__ import annotations

import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone

# Allow running this file as `python ml/train.py` from project root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.core.config import load_settings
from backend.app.services.yahoo_client import fetch_ohlcv
from ml.training.train_pipeline import train_symbol_horizon


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbols", default=None, help="Comma-separated symbols override")
    args = parser.parse_args()

    settings = load_settings()
    symbols = settings.symbols
    if args.symbols:
        symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]

    # Intraday training
    for symbol in symbols:
        print(f"[train] intraday symbol={symbol}")
        intraday_bars = fetch_ohlcv(
            symbol,
            interval=settings.intraday_interval,
            period=f"{settings.intraday_lookback_days}d",
        )
        if intraday_bars.empty:
            print(f"[train] skip {symbol} (no intraday data)")
            continue

        for horizon_m in settings.intraday_horizons_minutes:
            horizon = f"{horizon_m}m"
            try:
                path = train_symbol_horizon(
                    symbol=symbol,
                    timeframe="1m",
                    horizon=horizon,
                    bars=intraday_bars,
                    model_dir=settings.model_dir,
                    conformal_alpha=settings.conformal_alpha,
                )
                print(f"[train] saved {path}")
            except Exception as e:
                print(f"[train] failed {symbol} {horizon}: {e}")

        # Daily training
        print(f"[train] daily symbol={symbol}")
        daily_bars = fetch_ohlcv(symbol, interval="1d", period="2y")
        if daily_bars.empty:
            print(f"[train] skip {symbol} (no daily data)")
            continue

        daily_horizon = f"{settings.daily_horizon_days}d"
        try:
            path = train_symbol_horizon(
                symbol=symbol,
                timeframe="1d",
                horizon=daily_horizon,
                bars=daily_bars,
                model_dir=settings.model_dir,
                conformal_alpha=settings.conformal_alpha,
            )
            print(f"[train] saved {path}")
        except Exception as e:
            print(f"[train] failed {symbol} {daily_horizon}: {e}")


if __name__ == "__main__":
    main()

