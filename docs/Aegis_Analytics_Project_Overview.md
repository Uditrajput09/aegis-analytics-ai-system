# Aegis Analytics AI — Project Overview

Generated documentation for the full stack: data, ML, API, and dashboard.

---

## 1. Purpose

**Aegis Analytics AI** is an end-to-end market analytics application that:

- Pulls OHLCV bars from Yahoo Finance
- Engineers rolling and time-based features
- Trains ML models for short-horizon return and direction
- Serves forecasts and risk metrics over HTTP (FastAPI)
- Visualizes results in a Streamlit dashboard with user accounts

Default symbols (config): **RELIANCE.NS, INFY.NS, TCS.NS** (NSE-style tickers via yfinance).

Forecast horizons: **5m, 15m, 60m** (intraday, 1m bars) and **1d** (daily bars).

---

## 2. Architecture

```
Yahoo Finance (yfinance)
        |
        v
  ml/train.py  --------->  models/*.joblib
        |                        |
        v                        v
  data/app.db (SQLite)    backend predictor
        ^                        |
        |                        v
        +-------- FastAPI :8000 (JSON)
                        |
                        v
              Streamlit dashboard :8501
                        |
                        v
              data/dashboard_users.db (SQLite)
```

---

## 3. Technology Stack

| Layer | Technologies |
|-------|----------------|
| Runtime | Python 3.10+ |
| API | FastAPI, Uvicorn, Pydantic |
| UI | Streamlit, Plotly, custom CSS (theme.py) |
| ML | LightGBM (regression + classification), scikit-learn (isotonic calibration), NumPy, pandas |
| Market data | yfinance |
| API storage | SQLAlchemy + SQLite (bars, predictions) |
| Dashboard storage | sqlite3 (users, preferences, watchlist, history) |
| Model files | joblib (.joblib artifacts) |
| HTTP (dashboard) | requests → API_BASE_URL |

Dependencies are listed in `requirements.txt` at the project root.

---

## 4. Repository Layout

| Path | Role |
|------|------|
| backend/ | FastAPI: config, features, predictor, risk, Yahoo client, storage |
| ml/ | Training CLI, pipeline, calibration, conformal intervals |
| dashboard/ | Streamlit app, theme, user store, assistant module |
| models/ | Trained model artifacts |
| data/ | app.db, dashboard_users.db |
| scripts/ | deploy.ps1, restart.ps1, health_check.ps1, start_api/dashboard |
| .streamlit/config.toml | Dark Streamlit theme |

---

## 5. Configuration (Environment Variables)

| Variable | Purpose |
|----------|---------|
| SYMBOLS | Comma-separated tickers to train/serve |
| DATA_DB_PATH | API SQLite path (default data/app.db) |
| MODEL_DIR | Model directory (default models) |
| INTRADAY_INTERVAL | Yahoo interval (default 1m) |
| INTRADAY_LOOKBACK_DAYS | Intraday history window |
| DAILY_HORIZON_DAYS | Daily horizon in days |
| CONFORMAL_ALPHA | Miscoverage level for intervals (default 0.1) |
| API_BASE_URL | Dashboard → API URL (default http://127.0.0.1:8000) |

Settings loader: `backend/app/core/config.py`.

---

## 6. Data & Feature Pipeline

1. **Ingest:** `yahoo_client.py` — fetch OHLCV, normalize columns.
2. **Store:** `storage.py` — upsert bars and prediction snapshots.
3. **Features:** `feature_builder.py` — returns, rolling stats, MA trends, cyclical time features.
4. **Train:** `train_pipeline.py` — time-ordered splits; LGBM reg + clf; isotonic calibration; conformal residuals.
5. **Infer:** `predictor.py` — load artifact, latest features, return forecast + cache.

Artifact naming example: `{SYMBOL}_{timeframe}_{horizon}_mvp_v1.joblib`.

---

## 7. HTTP API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | / | Service info |
| GET | /health | Liveness |
| GET | /meta/symbols | Symbols with trained models |
| GET | /bars/recent | Recent OHLCV (DB + Yahoo backfill) |
| GET | /predictions/latest | Expected return, price, p_up, intervals |
| GET | /risk/latest | P(return < -1%), P(return < -2%) |

Interactive docs: `/docs` (Swagger), `/redoc`.

Query params: `symbol`, `horizon` (e.g. 5m, 1d), `timeframe` (1m or 1d), `force_update` (predictions).

---

## 8. ML Outputs

- **Expected return** — regression forecast for the horizon
- **Expected price** — last_close × (1 + expected_return)
- **p_up** — calibrated probability of upward move
- **interval_low / interval_high** — conformal return band
- **Risk** — tail probabilities derived from interval (MVP uniform assumption)

---

## 9. Dashboard Features

**Authentication:** Local SQLite users; demo account demo / demo123.

**User data:** Preferences, watchlist, prediction history; schema for strategies and trade records.

**Tabs:** Markets, Forecast, Risk, Account, Data.

**Assistant hub:** Strategy notes, trade logging, chat (template-based; `assistant.py` for richer Q&A logic).

**Charts:** Plotly price/volume, forecast projection, risk gauge, histograms.

---

## 10. Databases

| File | Used by | Contents |
|------|---------|----------|
| data/app.db | Backend | Bars, cached predictions |
| data/dashboard_users.db | Dashboard | Users, prefs, watchlist, history |

---

## 11. Local Run & Deploy

```powershell
pip install -r requirements.txt
python -m ml.train --symbols RELIANCE.NS,INFY.NS,TCS.NS
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
streamlit run dashboard/app.py --server.port 8501
```

Or: `.\scripts\deploy.ps1` (Windows).

Dashboard: http://localhost:8501  
API: http://127.0.0.1:8000/docs

---

## 12. Limitations & Notes

- Yahoo polling; not a live broker feed.
- MVP risk model from conformal interval.
- Dashboard signals are model-assisted, not financial advice.
- Assistant is not an external LLM API.
- Password hashing is SHA-256 (demo-grade).

---

*Document generated for project_type_02 / Aegis Analytics AI.*
