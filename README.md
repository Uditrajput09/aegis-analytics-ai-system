# Aegis Analytics AI

Pipeline for intraday/daily OHLCV features, ML forecasts (expected return, calibrated direction, conformal intervals), and a small FastAPI service plus Streamlit dashboard.

## What it does

- Pulls OHLCV bars from Yahoo Finance on a schedule (polling)
- Builds rolling features from historical + latest bars
- Trains ML models to forecast next-horizon returns / direction
- Produces:
  - Expected return (regression)
  - Direction confidence (`p_up`) via probability calibration
  - Prediction intervals via conformal residuals
- Provides:
  - FastAPI JSON endpoints ([Interactive docs](http://127.0.0.1:8000/docs) when the API is running)
  - A Streamlit dashboard for visualization and a risk panel



## Prerequisites

- Python 3.10+ recommended
- Working directory for commands: **project root** (the folder that contains `backend/`, `ml/`, and `dashboard/`)



## Quick start (local)

1. Create a virtual environment and install dependencies:
  ```bash
   pip install -r requirements.txt
  ```
2. Train models (required before `/predictions/latest` and `/risk/latest` can compute fresh results; intraday horizons are 5m, 15m, 60m plus one daily horizon from config):
  ```bash
   python -m ml.train --symbols AAPL
  ```
   Equivalent: `python ml/train.py --symbols AAPL`
3. Start the API (from project root):
  ```bash
   python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
  ```
   Windows helper (detects port already in use):
   If you see **WinError 10048**, port `8000` is already taken — the API may already be running. Check `ht` python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
   Windows helper:
   If the API uses another host or port, set `API_BASE_URL` (for example `http://127.0.0.1:8000`) before launching Streamlit.
   **Deploy or fix a broken/stale site (Windows):**



### Troubleshooting


| Symptom                             | Fix                                                     |
| ----------------------------------- | ------------------------------------------------------- |
| `WinError 10048` on API start       | Port 8000 in use — run `.\scripts\restart.ps1`          |
| Site looks old or broken            | Old process still running — run `.\scripts\restart.ps1` |
| Dashboard: "API unreachable"        | Start the API first (step 3)                            |
| Dashboard: "Missing model artifact" | Train that symbol: `python -m ml.train --symbols AAPL`  |
| Only use symbols with models        | Dashboard lists trained symbols via `GET /meta/symbols` |




## HTTP API


| Method | Path                  | Description                                                                           |
| ------ | --------------------- | ------------------------------------------------------------------------------------- |
| GET    | `/`                   | Service name, status, and route hints                                                 |
| GET    | `/health`             | Liveness; returns `ok` and `time_utc` (UTC ISO timestamp)                             |
| GET    | `/bars/recent`        | Recent stored bars; may fetch from Yahoo if the DB is empty for that symbol/timeframe |
| GET    | `/predictions/latest` | Latest forecast for symbol + horizon                                                  |
| GET    | `/risk/latest`        | Risk metrics derived from the latest prediction interval                              |


OpenAPI: `http://127.0.0.1:8000/docs` (Swagger UI) and `http://127.0.0.1:8000/redoc`.

### Example queries

- `GET http://127.0.0.1:8000/bars/recent?symbol=AAPL&timeframe=1m&limit=300`
- `GET http://127.0.0.1:8000/predictions/latest?symbol=AAPL&horizon=5m`
- `GET http://127.0.0.1:8000/risk/latest?symbol=AAPL&horizon=5m`

Query parameters:

- `timeframe` (bars): `1m` or `1d`
- `horizon` (predictions / risk): minute or day suffix, e.g. `5m`, `15m`, `60m`, `1d` (timeframe is inferred from the horizon unless you pass `timeframe` explicitly; it must match the inference)
- `force_update` (predictions / risk): `true` to recompute instead of using the latest cached prediction when possible

If model artifacts are missing or Yahoo data cannot be loaded, prediction routes respond with **503** and a clear `detail` message instead of an unhandled error.

## Configuration

Environment variables (defaults in `backend/app/core/config.py`):


| Variable                     | Role                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| `SYMBOLS`                    | Comma-separated tickers (default `AAPL,MSFT,GOOGL`)          |
| `DATA_DB_PATH`               | SQLite database file (default `data/app.db`)                 |
| `MODEL_DIR`                  | Directory for trained `.joblib` artifacts (default `models`) |
| `INTRADAY_INTERVAL`          | Yahoo interval for intraday pulls (default `1m`)             |
| `INTRADAY_LOOKBACK_DAYS`     | Intraday history window (default `7`)                        |
| `DAILY_HORIZON_DAYS`         | Daily horizon label in days (default `1`)                    |
| `PREDICTION_REFRESH_MINUTES` | Used by scheduling / refresh logic (default `5`)             |
| `CONFORMAL_ALPHA`            | Conformal miscoverage level (default `0.1`)                  |


Intraday training horizons are fixed in code at 5, 15, and 60 minutes unless you change `backend/app/core/config.py`.