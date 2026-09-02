# Aegis Analytics AI

> **Enterprise Quantitative Market Intelligence, Calibrated ML Forecasting & Web3 Cryptographic Verification Platform**

Aegis Analytics AI is an institutional-grade quantitative finance platform designed for multi-asset return forecasting, directional probability calibration, distribution-free statistical risk bounds (conformal prediction), and tamper-proof on-chain audit verification using EVM smart contracts.

---

## ⚡ Core Capabilities & Highlights

- **Dual-Head Machine Learning**: Simultaneous LightGBM regression ($\hat{y}_{\text{return}}$) and classification ($y_{\text{up}}$) for multi-horizon forecasts (`5m`, `15m`, `60m`, `1d`).
- **Mathematical Confidence & Risk**:
  - **Isotonic Probability Calibration**: Converts raw classification tree outputs into true, calibrated directional confidence ($p_{\text{up}}$).
  - **Conformal Prediction Intervals**: Non-parametric absolute residual quantile estimation guaranteeing $(1 - \alpha)$ statistical coverage (default 90%).
  - **Downside Tail-Risk Analytics**: Mathematical estimation of tail-event downside probabilities ($P(\text{Return} < -1\%)$ and $P(\text{Return} < -2\%)$).
- **Web3 & Blockchain Audit Trail**:
  - Solidity smart contracts (`PriceAnchor.sol` and `PredictionAudit.sol`) deployed via Hardhat to Sepolia / Polygon networks.
  - Cryptographic SHA-256 hash anchoring of historical prices and model predictions for verifiable auditability.
  - Chainlink decentralized price oracle integration and block explorer verification links.
- **Multi-Asset Market Ingestion**:
  - Traditional Equities & Indices: Yahoo Finance (`yfinance`) with automatic caching and retry resilience.
  - Spot Cryptocurrency: Binance REST / WebSocket client & CoinGecko API.
  - Decentralized Finance (DeFi): Protocol Total Value Locked (TVL) via DeFiLlama & Uniswap V3 liquidity metrics via The Graph.
- **Dual Presentation Ecosystem**:
  - **React 19 SPA**: Modern TypeScript + Vite 8 + Tailwind CSS v4 + Recharts application featuring 12 dedicated analytical modules.
  - **Streamlit Dashboard**: Interactive Python dashboard with Plotly candlestick charting, AI Assistant, and user authentication.
- **Enterprise Storage & Migrations**:
  - PostgreSQL 16 with TimescaleDB hypertables for high-throughput time-series data.
  - Alembic database migrations (`backend/app/db/migrations/`).
  - Zero-config SQLite local development fallback (`data/app.db`).

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend SPA** | React 19, TypeScript 6, Vite 8, Tailwind CSS v4, Recharts 3, Lucide React, Oxlint |
| **Backend REST API** | FastAPI, Uvicorn, Pydantic v2, Pydantic-Settings, HTTPX, Tenacity |
| **Machine Learning** | LightGBM, Scikit-Learn (`IsotonicRegression`), Pandas, NumPy, Joblib |
| **Smart Contracts & Web3** | Solidity 0.8.20, Hardhat, Web3.py, Eth-Account, Hexbytes, Etherscan / Polygonscan |
| **Database & ORM** | PostgreSQL 16 + TimescaleDB, Alembic, SQLAlchemy 2.0, SQLite (Local Dev Fallback) |
| **Data Providers** | Yahoo Finance (`yfinance`), Binance (`python-binance`), CoinGecko (`pycoingecko`), DeFiLlama, The Graph |
| **Alternative Dashboard** | Streamlit, Plotly |
| **DevOps & Orchestration** | Docker Compose, PowerShell Automation Scripts |

---

## 📁 Repository Structure

```
project_type_02/
├── backend/                       # FastAPI Backend Core
│   └── app/
│       ├── api/                   # REST route handlers & endpoint index
│       ├── blockchain/            # Web3.py chain client, anchor service & oracle service
│       ├── core/                  # Configuration dataclass & Pydantic schemas
│       ├── db/                    # Alembic migration environment & version scripts
│       ├── features/              # Feature engineering & cyclical time encodings
│       ├── risk/                  # Tail risk probability calculation engine
│       ├── services/              # In-memory predictor, storage manager, crypto/defi/yahoo clients
│       └── main.py                # FastAPI server entry point
├── contracts/                     # Solidity Smart Contracts & Deployment Scripts
│   ├── PredictionAudit.sol        # On-chain ML forecast audit contract
│   ├── PriceAnchor.sol            # On-chain OHLCV bar anchor contract
│   └── scripts/                   # Hardhat deployment scripts
├── dashboard/                     # Streamlit Interactive Dashboard
│   ├── app.py                     # Main dashboard layout
│   ├── assistant.py               # Embedded AI market assistant
│   ├── theme.py                   # Custom glassmorphism design system & Plotly themes
│   └── user_store.py              # SQLite user authentication & watchlists
├── docs/                          # In-depth system documentation
│   └── Aegis_Analytics_Project_Overview.md
├── frontend/                      # React 19 + TypeScript + Vite + Tailwind CSS v4 Web App
│   ├── src/
│   │   ├── components/            # Reusable UI & auth components
│   │   ├── layouts/               # Responsive sidebar & header shell (AppLayout.tsx)
│   │   ├── pages/                 # 12 application view pages
│   │   ├── services/              # Typed API client (api.ts)
│   │   └── types/                 # TypeScript contract definitions
│   └── package.json
├── ml/                            # Machine Learning Engine
│   ├── confidence/                # Isotonic calibration & conformal prediction intervals
│   ├── training/                  # Train/calibration split pipeline & joblib exporter
│   └── train.py                   # Multi-symbol training CLI
├── models/                        # Serialized .joblib model artifacts
├── scripts/                       # PowerShell operational & deployment scripts
├── docker-compose.yml             # PostgreSQL/TimescaleDB, API, and Dashboard container setup
├── hardhat.config.js              # Hardhat EVM network configuration
├── requirements.txt               # Python backend dependencies
└── README.md
```

---

## 🚀 Quick Start (Local Setup)

### 1. Prerequisites
- **Python**: 3.10 or higher
- **Node.js**: 18.x or higher (Node 20+ recommended)
- **Git**

### 2. Backend & ML Setup
```powershell
# 1. Clone repository and navigate to project root
git clone https://github.com/Uditrajput09/aegis-analytics-ai-system.git
cd aegis-analytics-ai-system

# 2. Create and activate Python virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Train ML models across default tickers (creates models/*.joblib artifacts)
python -m ml.train --symbols RELIANCE.NS,INFY.NS,TCS.NS,AAPL,MSFT

# 5. Start the FastAPI backend server (http://127.0.0.1:8000)
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
# Alternatively on Windows: .\scripts\start_api.ps1
```

### 3. Frontend Web App Setup (React 19 + Vite)
```bash
# Open a new terminal in the frontend directory
cd frontend

# Install Node dependencies
npm install

# Start Vite development server (http://localhost:5173)
npm run dev
```

### 4. Alternative Streamlit Dashboard Setup
```powershell
# Open a new terminal in the project root
streamlit run dashboard/app.py
# Alternatively on Windows: .\scripts\start_dashboard.ps1
```

### 5. Docker Compose Launch
Run PostgreSQL/TimescaleDB, FastAPI, and Streamlit in orchestrated containers:
```bash
docker-compose up -d
```

---

## ⛓️ Smart Contract Deployment (Hardhat)

Deploy the `PriceAnchor.sol` and `PredictionAudit.sol` contracts to a local or testnet EVM node:

```bash
# Run local Hardhat node
npx hardhat node

# In a separate terminal, deploy contracts
npx hardhat run contracts/scripts/deploy.js --network localhost

# Deploy to Sepolia testnet (requires WALLET_PRIVATE_KEY & CHAIN_RPC_URL in .env)
npx hardhat run contracts/scripts/deploy.js --network sepolia
```

---

## 🌐 HTTP REST API Reference

Interactive Swagger documentation is available at `http://127.0.0.1:8000/docs` and ReDoc at `http://127.0.0.1:8000/redoc`.

| Method | Endpoint | Query Parameters | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | None | API service information, root status, and route catalog |
| `GET` | `/health` | None | Liveness check returning `ok` and UTC ISO timestamp |
| `GET` | `/meta/symbols` | None | List of ticker symbols with trained `.joblib` model artifacts |
| `GET` | `/bars/recent` | `symbol`, `timeframe` (`1m`/`1d`), `limit` | Historical OHLCV bars with automatic on-demand ingestion |
| `GET` | `/predictions/latest` | `symbol`, `horizon` (`5m`/`15m`/`60m`/`1d`), `timeframe`, `force_update` | Latest ML return prediction, $p_{\text{up}}$ confidence & conformal interval |
| `GET` | `/risk/latest` | `symbol`, `horizon`, `timeframe`, `force_update` | Downside tail-risk probabilities ($P(\text{Return} < -1\%)$ / $-2\%$) |
| `POST` | `/auth/login` | JSON body (`username`, `password`) | Authenticate user and return session token |
| `POST` | `/auth/register` | JSON body (`username`, `password`) | Register a new user account |
| `GET` | `/blockchain/status` | None | Web3 RPC connection state, chain ID, and contract addresses |
| `GET` | `/blockchain/anchors/{symbol}` | `symbol`, `limit` | Query on-chain anchor history for a specific symbol |
| `GET` | `/blockchain/verify/{tx_hash}` | `tx_hash` (path param) | Verify cryptographic SHA-256 hash and block explorer link |
| `POST` | `/blockchain/anchor-prediction`| `symbol`, `horizon`, `timeframe` | Manually anchor a prediction snapshot to the blockchain |
| `GET` | `/oracle/prices/{pair}` | `pair` (e.g. `ETH/USD`, `AAPL`) | Chainlink decentralized oracle price with fallback resolver |
| `GET` | `/crypto/symbols` | None | Supported cryptocurrency pairs on Binance / CoinGecko |
| `GET` | `/crypto/bars/recent` | `symbol` (e.g. `BTCUSDT`), `interval`, `limit` | Crypto OHLCV bar history from Binance |
| `GET` | `/defi/protocols` | None | Supported DeFi protocol slugs |
| `GET` | `/defi/tvl/{protocol}` | `protocol` (e.g. `aave`, `uniswap`) | Total Value Locked (TVL) from DeFiLlama |
| `GET` | `/defi/global` | None | Global aggregate DeFi TVL and market statistics |
| `GET` | `/defi/uniswap/pools` | `limit` | Top Uniswap V3 liquidity pools via The Graph |

---

## ⚙️ Configuration & Environment Matrix

All settings can be configured via `.env` file or system environment variables (defaults in `backend/app/core/config.py`):

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `SYMBOLS` | String | `RELIANCE.NS,INFY.NS,TCS.NS` | Comma-separated default equity tickers |
| `DATABASE_URL` | String | `sqlite:///data/app.db` | PostgreSQL connection URL (e.g. `postgresql+psycopg2://user:pass@localhost:5432/aegis`) |
| `DATA_DB_PATH` | Path | `data/app.db` | Fallback SQLite database path for local development |
| `MODEL_DIR` | Path | `models` | Directory for serialized `.joblib` model files |
| `INTRADAY_INTERVAL` | String | `1m` | Yahoo Finance interval for intraday bars |
| `INTRADAY_LOOKBACK_DAYS` | Integer | `7` | Historical days window for intraday bar retrieval |
| `DAILY_HORIZON_DAYS` | Integer | `1` | Daily forecast horizon in days |
| `CONFORMAL_ALPHA` | Float | `0.1` | Conformal miscoverage level ($0.10 = 90\%$ statistical confidence) |
| `BLOCKCHAIN_ENABLED` | Boolean | `false` | Enable/disable Web3 on-chain anchoring |
| `CHAIN_RPC_URL` | String | `""` | EVM RPC endpoint (Infura, Alchemy, or Localhost) |
| `CHAIN_ID` | Integer | `11155111` | EVM Chain ID (11155111 = Sepolia, 137 = Polygon, 1 = Mainnet) |
| `WALLET_PRIVATE_KEY` | String | `""` | Signing wallet private key for on-chain transactions |
| `PRICE_ANCHOR_CONTRACT` | Address | `""` | Deployed address for `PriceAnchor.sol` |
| `PREDICTION_AUDIT_CONTRACT` | Address | `""` | Deployed address for `PredictionAudit.sol` |
| `BINANCE_API_KEY` | String | `""` | Binance API key for spot market access |
| `COINGECKO_API_KEY` | String | `""` | CoinGecko API key for crypto data |

---

## 🔧 Operational Troubleshooting

| Symptom | Probable Cause | Recommended Action |
| :--- | :--- | :--- |
| `WinError 10048` on backend start | Port 8000 is occupied by a background Python process | Run `.\scripts\restart.ps1` to cleanly terminate and restart processes |
| `503 Missing model artifact` | Model `.joblib` has not been trained for the requested symbol | Train the symbol: `python -m ml.train --symbols <SYMBOL>` |
| `400 Timeframe mismatch` | Horizon timeframe (`5m` = `1m`) does not match explicit `timeframe` param | Omit `timeframe` parameter to allow automatic inference |
| Web3 anchoring fails / skipped | `BLOCKCHAIN_ENABLED=false` or missing RPC / private key | Set `BLOCKCHAIN_ENABLED=true` and supply valid `CHAIN_RPC_URL` and `WALLET_PRIVATE_KEY` |
| PostgreSQL connection fails | Database container is not running | Launch database via `docker-compose up -d postgres` or rely on SQLite fallback |