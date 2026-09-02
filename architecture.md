# Aegis Analytics AI System — Architecture Specification & Graph

---

## 🏛️ 1. High-Level System Overview

```mermaid
graph TB
    subgraph CLIENT_LAYER["🖥️ Client & Presentation Layer"]
        FE["React 19 + TypeScript + Vite 8\nTailwind CSS v4 · Recharts · Lucide\n(12 Dedicated Application Pages)"]
        DASH["Streamlit Dashboard\nGlassmorphism Theme · Plotly Charts\nEmbedded AI Assistant"]
    end

    subgraph BACKEND_LAYER["⚙️ Backend & API Layer (FastAPI / Python 3.10+)"]
        API["FastAPI Router\n/api/routes.py · /api/index.py"]
        CORE["Core Module\nconfig.py · types.py"]
        
        subgraph SERVICES["Business Logic & Integration Services"]
            PRED["Predictor Engine\n(In-Memory Artifacts)"]
            STORE["Storage Manager\n(PostgreSQL / TimescaleDB / SQLite)"]
            CRYPTO_S["Crypto Client\n(Binance REST/WS + CoinGecko)"]
            DEFI_S["DeFi Client\n(DeFiLlama TVL + Uniswap The Graph)"]
            YAHOO_S["Yahoo Client\n(OHLCV Resilient Ingestion)"]
        end

        subgraph ML_INTEGRATION["Machine Learning & Risk Core"]
            FEAT["Feature Builder\n(Vectorized Returns & Cyclical Encodings)"]
            RISK["Risk Engine\n(Downside Tail Risk & Conformal Bounds)"]
        end

        subgraph BLOCKCHAIN_LAYER["⛓️ Web3 & Blockchain Engine"]
            ORACLE_SVC["Oracle Service\n(Chainlink Price Feeds)"]
            ANCHOR_SVC["Anchor Service\n(Cryptographic SHA-256 Hashing)"]
            CHAIN_CLI["Chain Client\n(Web3.py Connection Manager)"]
            EVT_LST["Event Listener\n(On-Chain Event Polling)"]
        end
    end

    subgraph ML_LAYER["🤖 Machine Learning Pipeline"]
        TRAIN_CLI["Training Pipeline CLI\n(ml/train.py)"]
        LGBM_HEADS["Dual-Head LightGBM\n(Regressor + Classifier)"]
        CALIB["Isotonic Probability Calibrator\n(p_up Calibration)"]
        CONF["Conformal Residual Quantiles\n(90% Coverage Bounds)"]
    end

    subgraph SMART_CONTRACTS["📜 Smart Contracts (Solidity 0.8.20 / Hardhat)"]
        PA_CONTRACT["PredictionAudit.sol\n(Immutable Forecast Anchoring)"]
        PRC_CONTRACT["PriceAnchor.sol\n(Historical OHLCV Integrity)"]
    end

    subgraph DATA_LAYER["🗄️ Persistence & Storage Layer"]
        PG_DB[("PostgreSQL 16 + TimescaleDB\nHypertables for OHLCV & Anchors\nAlembic Migrations")]
        SQLITE_DB[("SQLite Local Fallback\ndata/app.db · dashboard_users.db")]
        MODEL_STORE[("Model Artifacts Store\nmodels/*.joblib")]
    end

    subgraph EXTERNAL_PROVIDERS["🌐 External Data & Network Feeds"]
        YAHOO_API["Yahoo Finance API\n(Equities & Indices)"]
        BINANCE_API["Binance API\n(Crypto Spot OHLCV)"]
        COINGECKO_API["CoinGecko API\n(Market Cap & Fallback Prices)"]
        DEFILLAMA_API["DeFiLlama API\n(Global TVL & Protocols)"]
        THEGRAPH_API["The Graph Subgraphs\n(Uniswap V3 Pools)"]
        EVM_NODES["EVM RPC Nodes\n(Sepolia · Polygon · Localhost)"]
    end

    %% Client Interactions
    FE -- "REST JSON HTTP" --> API
    DASH -- "REST JSON HTTP" --> API

    %% Backend Routing
    API --> CORE
    API --> SERVICES
    API --> ML_INTEGRATION
    API --> BLOCKCHAIN_LAYER

    %% Service Connections
    PRED --> MODEL_STORE
    PRED --> FEAT
    PRED --> STORE
    STORE --> PG_DB
    STORE --> SQLITE_DB
    YAHOO_S --> YAHOO_API
    CRYPTO_S --> BINANCE_API
    CRYPTO_S --> COINGECKO_API
    DEFI_S --> DEFILLAMA_API
    DEFI_S --> THEGRAPH_API

    %% ML Engine Links
    TRAIN_CLI --> FEAT
    TRAIN_CLI --> LGBM_HEADS
    LGBM_HEADS --> CALIB
    LGBM_HEADS --> CONF
    CALIB & CONF --> MODEL_STORE
    RISK --> CONF

    %% Blockchain Engine Links
    CHAIN_CLI --> EVM_NODES
    ANCHOR_SVC --> CHAIN_CLI
    ANCHOR_SVC --> PRC_CONTRACT
    ANCHOR_SVC --> PA_CONTRACT
    ORACLE_SVC --> CHAIN_CLI
    EVT_LST --> CHAIN_CLI
```

---

## 💻 2. Frontend Application Architecture (React 19 + TypeScript + Vite)

```mermaid
graph LR
    subgraph FRONTEND_CORE["Frontend Architecture (React 19 + Vite 8)"]
        ENTRY["main.tsx"] --> APP["App.tsx\n(View Controller & State)"]
        APP --> LAYOUT["AppLayout.tsx\n(Sidebar, Header Status, Toasts)"]

        subgraph APP_PAGES["12 Application Pages"]
            P1["OverviewPage"]
            P2["MarketAnalyticsPage"]
            P3["ForecastsPage"]
            P4["RiskAnalyticsPage"]
            P5["CryptoDefiPage"]
            P6["AIAnalystPage"]
            P7["BlockchainAuditPage"]
            P8["InsightsPage"]
            P9["ReportsPage"]
            P10["WatchlistPage"]
            P11["SettingsPage"]
            P12["LoginPage"]
        end

        subgraph DESIGN_SYSTEM["Styling & Telemetry"]
            CSS["index.css / App.css\n(Tailwind CSS v4 + Glassmorphism)"]
            CHARTS["Recharts 3.x\n(Candlestick, Area, Gauge, Bar)"]
            ICONS["Lucide React Icons"]
        end

        subgraph CLIENT_SERVICES["Frontend Service Layer"]
            API_CLIENT["services/api.ts\n(Typed Axios/Fetch Gateway)"]
            TYPES["types/api.ts\n(Contract Interfaces)"]
        end

        LAYOUT --> APP_PAGES
        APP_PAGES --> CHARTS
        APP_PAGES --> ICONS
        APP_PAGES --> API_CLIENT
        API_CLIENT --> TYPES
    end
```

---

## ⚙️ 3. Backend & Blockchain Service Architecture

```mermaid
graph TB
    subgraph BACKEND_STRUCTURE["FastAPI Backend Architecture"]
        MAIN_APP["main.py\n(FastAPI Entry & Lifespan)"]
        ROUTES_LAYER["api/routes.py\n(All REST Route Handlers)"]

        subgraph SERVICE_MODULES["Core Service Modules"]
            PREDICTOR["predictor.py\n• Model Artifact Cache\n• Dynamic Feature Vector Ingestion\n• Expected Price & Conformal Bounds"]
            STORAGE_MOD["storage.py\n• PostgreSQL/TimescaleDB Pool\n• SQLite Fallback Engine\n• Upsert & Query Manager"]
            RISK_MOD["risk_engine.py\n• Tail-Risk Downside Estimation\n• Uniform Residual Density Integration"]
            FEAT_BUILDER["feature_builder.py\n• Multi-Period Returns (k=1,2,3,5)\n• Rolling Moments (Mean, Std)\n• Moving Average Distances\n• Sin/Cos Cyclical Time Features"]
        end

        subgraph BLOCKCHAIN_MODULES["Blockchain & Smart Contract Modules"]
            ANCHOR_MOD["anchor_service.py\n• Hash Computation (SHA-256)\n• Price & Prediction On-Chain Anchors\n• Auto-Seeding & Database Audit Sync"]
            CHAIN_MOD["chain_client.py\n• Web3.py RPC Connection\n• Nonce & Gas Management\n• Multi-Network Switcher"]
            ORACLE_MOD["oracle_service.py\n• Chainlink Decentralized Feeds\n• Off-Chain Fallback Resolvers"]
            LISTENER_MOD["event_listener.py\n• Contract Event Filtering\n• Block Confirmation Validation"]
        end

        subgraph EXTERNAL_CONNECTORS["Market Data Connectors"]
            CRYPTO_MOD["crypto_client.py\n• Binance REST/WS\n• CoinGecko Fallback"]
            DEFI_MOD["defi_client.py\n• DeFiLlama TVL API\n• The Graph Uniswap V3 Subgraph"]
            YAHOO_MOD["yahoo_client.py\n• yfinance Ingestion\n• Resilient Exponential Retries"]
        end

        MAIN_APP --> ROUTES_LAYER
        ROUTES_LAYER --> SERVICE_MODULES
        ROUTES_LAYER --> BLOCKCHAIN_MODULES
        ROUTES_LAYER --> EXTERNAL_CONNECTORS
        CHAIN_MOD --> ANCHOR_MOD
        CHAIN_MOD --> ORACLE_MOD
        CHAIN_MOD --> LISTENER_MOD
    end
```

---

## 🔄 4. Data Flow & Execution Sequences

### A. Prediction Ingestion & Cryptographic On-Chain Anchoring
```mermaid
sequenceDiagram
    autonumber
    actor Client as User / Frontend
    participant API as FastAPI Backend (/predictions/latest)
    participant FB as FeatureBuilder
    participant Pred as Predictor (LightGBM)
    participant Store as Storage (PostgreSQL/TimescaleDB)
    participant Anchor as AnchorService (Web3.py)
    participant Chain as PredictionAudit.sol (EVM)

    Client->>API: GET /predictions/latest?symbol=AAPL&horizon=5m
    API->>Store: Check cached prediction snapshot
    alt Cache Miss or force_update=True
        API->>Store: fetch_bars(symbol, timeframe='1m')
        Store-->>API: OHLCV Bar DataFrame
        API->>FB: build_features_for_inference(df)
        FB-->>API: Feature Vector (x_t)
        API->>Pred: predict(x_t) via .joblib artifact
        Pred-->>API: expected_return, p_up, interval_low, interval_high
        API->>Store: save_prediction(record)
        opt Blockchain Enabled
            API->>Anchor: anchor_prediction(record)
            Anchor->>Anchor: Compute SHA-256(symbol, horizon, ts, return, bounds)
            Anchor->>Chain: recordPredictionAudit(hash, symbol, return, low, high)
            Chain-->>Anchor: Transaction Receipt (tx_hash, block_number)
            Anchor->>Store: save_blockchain_anchor(record)
        end
    end
    API-->>Client: Prediction JSON (Telemetry, p_up, Conformal Bounds, tx_hash)
```

### B. On-Chain Cryptographic Verification Workflow
```mermaid
sequenceDiagram
    autonumber
    actor Auditor as External Auditor / Client
    participant API as FastAPI Backend (/blockchain/verify/{tx_hash})
    participant Store as Storage (PostgreSQL/TimescaleDB)
    participant Chain as EVM Block Explorer (Etherscan/Polygonscan)

    Auditor->>API: GET /blockchain/verify/{tx_hash}
    API->>Store: Query blockchain_anchors table
    Store-->>API: Anchor Metadata (data_hash, block_number, chain_id, gas_used)
    API->>API: Construct verified explorer URL
    API-->>Auditor: Verification JSON (Valid=True, Explorer URL, Cryptographic Hash)
    Auditor->>Chain: Inspect on-chain event log & parameters
```

---

## 🗄️ 5. Database & Migration Schema Architecture

```mermaid
erDiagram
    BARS {
        string symbol PK
        string timeframe PK
        datetime ts_utc PK
        float open
        float high
        float low
        float close
        bigint volume
    }

    PREDICTIONS {
        string symbol PK
        string timeframe PK
        string horizon PK
        datetime base_ts_utc PK
        datetime created_ts_utc
        float last_close
        float expected_return
        float expected_price
        float p_up
        float interval_low
        float interval_high
        string model_version
        datetime model_timestamp_utc
    }

    BLOCKCHAIN_ANCHORS {
        int id PK
        string anchor_type
        string ref_symbol
        string ref_horizon
        datetime ref_ts_utc
        string data_hash
        string tx_hash UK
        bigint block_number
        int chain_id
        bigint gas_used
        datetime created_at
    }

    USERS {
        int id PK
        string username UK
        string password_hash
        string email
        datetime created_at
        datetime last_login
    }

    BARS ||--o{ PREDICTIONS : "features derived from"
    PREDICTIONS ||--o{ BLOCKCHAIN_ANCHORS : "cryptographically audited by"
```

---

## 📊 6. Technology Stack Matrix

| Layer | Primary Technology | Key Packages & Versions | Purpose & Capabilities |
| :--- | :--- | :--- | :--- |
| **Frontend SPA** | React 19 + TypeScript 6 + Vite 8 | `react: ^19.2.8`, `typescript: ~6.0.2`, `vite: ^8.2.0`, `tailwindcss: ^4.3.3`, `recharts: ^3.10.1`, `lucide-react: ^1.31.0`, `oxlint: ^1.75.0` | 12 dedicated financial analytics pages, real-time charts, glassmorphic dark design system |
| **Backend REST API** | FastAPI + Uvicorn | `fastapi`, `uvicorn[standard]`, `pydantic`, `pydantic-settings`, `httpx` | High-throughput asynchronous REST API serving predictions, risk, market data, and Web3 endpoints |
| **Machine Learning** | LightGBM + Scikit-Learn | `lightgbm`, `scikit-learn`, `joblib`, `numpy`, `pandas` | Dual-head regression and classification, Isotonic probability calibration, Conformal prediction bounds |
| **Smart Contracts** | Solidity 0.8.20 + Hardhat | `@nomicfoundation/hardhat-toolbox`, `dotenv` | `PriceAnchor.sol` and `PredictionAudit.sol` for immutable on-chain data verification |
| **Web3 Client** | Web3.py + Eth-Account | `web3>=6.15.0`, `eth-account>=0.10.0`, `hexbytes>=0.3.0` | Transaction signing, smart contract interaction, event polling, Chainlink price feed queries |
| **Database & ORM** | PostgreSQL 16 + TimescaleDB | `psycopg2-binary>=2.9.9`, `asyncpg>=0.29.0`, `alembic>=1.13.0`, `sqlalchemy` | High-performance time-series hypertables, Alembic schema migrations, SQLite fallback |
| **Crypto & DeFi Data** | Binance + CoinGecko + DeFiLlama | `python-binance>=1.0.19`, `pycoingecko>=3.1.0`, The Graph Uniswap Subgraph | Multi-asset crypto spot OHLCV, protocol Total Value Locked (TVL), decentralized liquidity pool metrics |
| **Dashboard** | Streamlit + Plotly | `streamlit`, `plotly` | Standalone interactive quantitative dashboard, AI Assistant, and user management store |
| **DevOps & Infra** | Docker Compose + PowerShell | `docker-compose.yml`, PowerShell scripts (`scripts/`) | Containerized deployment of API, TimescaleDB, and Streamlit with automated restart/health scripts |
