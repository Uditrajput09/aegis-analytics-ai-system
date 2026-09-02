# Graph Report - project_type_02  (2026-09-01)

## Corpus Check
- Corpus is ~45,622 words - fits in a single context window. You may not need a graph.

## Summary
- 570 nodes · 1096 edges · 58 communities (19 shown, 17 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 23 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Frontend React UI & Components
- Authentication & Streamlit Dashboard
- FastAPI Endpoints & Architecture
- ML Predictor & Storage Service
- Frontend UI Dependencies & Styling
- Feature Engineering & Time Series Transforms
- TypeScript Client Configuration
- Node TypeScript Configuration
- Blockchain Anchor & Web3 Client
- Chainlink Oracle Service
- DeFi Protocol & TVL Metrics
- Blockchain Oracle Feeds
- Linting & Code Quality (Oxlint)
- Prediction & Price Anchoring
- Blockchain Event Listener
- Database Migrations (Alembic)
- Cryptographic Hashing & Anchor Tests
- Web3 Client & Oracle Tests
- Contextual AI Assistant
- Web3 Transaction Receipts
- Smart Contract Deployment
- Smart Contract Verification
- TypeScript Project References
- Blockchain Module Setup
- Test Suite Setup
- Aegis System Brain Context
- Docker Compose Orchestration
- Project Overview Documentation
- Frontend Asset: Favicon
- Frontend Asset: Icons
- Project Readme Documentation
- Frontend Asset: Hero Banner
- Frontend Asset: React Logo
- Frontend Asset: Vite Logo
- Project Specification Doc
- Frontend Readme Doc

## God Nodes (most connected - your core abstractions)
1. `main()` - 40 edges
2. `ChainClient` - 28 edges
3. `react` - 20 edges
4. `compilerOptions` - 18 edges
5. `load_settings()` - 17 edges
6. `predict_latest()` - 16 edges
7. `horizon_label()` - 15 edges
8. `apiService` - 15 edges
9. `compilerOptions` - 15 edges
10. `_make_engine()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `load_settings()`  [EXTRACTED]
  ml/train.py → backend/app/core/config.py
- `auth_login()` --calls--> `authenticate_user()`  [EXTRACTED]
  backend/app/api/routes.py → dashboard/user_store.py
- `auth_login()` --calls--> `get_or_create_demo_user()`  [EXTRACTED]
  backend/app/api/routes.py → dashboard/user_store.py
- `auth_login()` --calls--> `init_user_store()`  [EXTRACTED]
  backend/app/api/routes.py → dashboard/user_store.py
- `auth_register()` --calls--> `init_user_store()`  [EXTRACTED]
  backend/app/api/routes.py → dashboard/user_store.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Dual-Head LightGBM Forecasting & Conformal Risk Pipeline** — backend_app_services_predictor [INFERRED 0.95]

## Communities (58 total, 17 thin omitted)

### Community 0 - "Frontend React UI & Components"
Cohesion: 0.06
Nodes (57): App(), BrandLogo(), BrandLogoProps, FinancialVisualization(), HeroSection(), LoginCard(), LoginCardProps, AppLayout() (+49 more)

### Community 1 - "Authentication & Streamlit Dashboard"
Cohesion: 0.08
Nodes (69): auth_login(), auth_register(), AuthRequest, BaseModel, Connection, add_indicators(), api_ok(), build_advice() (+61 more)

### Community 2 - "FastAPI Endpoints & Architecture"
Cohesion: 0.07
Nodes (56): Aegis Analytics System Architecture, anchor_prediction_endpoint(), bars_recent(), blockchain_anchors(), blockchain_status(), crypto_bars_recent(), crypto_symbols(), defi_global() (+48 more)

### Community 3 - "ML Predictor & Storage Service"
Cohesion: 0.07
Nodes (56): blockchain_verify(), Look up an anchor record by its transaction hash and return verification status., anchor_service.py — Cryptographic hashing and on-chain anchoring service.…, _artifact_path(), _ensure_minimum_bars(), _load_artifact(), predict_latest(), PredictionOut (+48 more)

### Community 4 - "Frontend UI Dependencies & Styling"
Cohesion: 0.04
Nodes (45): autoprefixer, clsx, dependencies, clsx, lucide-react, react, react-dom, recharts (+37 more)

### Community 5 - "Feature Engineering & Time Series Transforms"
Cohesion: 0.08
Nodes (34): add_time_features(), _base_price_features(), build_features_and_targets(), build_latest_features(), _cyclical_features(), horizons_from_config(), HorizonSpec, DataFrame (+26 more)

### Community 6 - "TypeScript Client Configuration"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 7 - "Node TypeScript Configuration"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 8 - "Blockchain Anchor & Web3 Client"
Cohesion: 0.13
Nodes (11): AnchorService, Service to anchor prices and predictions on-chain and record audit trails., ChainClient, Wrapper around Web3 instance with safe connection handling and transaction…, Return True if Web3 connection to RPC node is active., Fetch current block height on target chain., Fetch current gas price in wei., Get ETH/MATIC balance for an address. (+3 more)

### Community 9 - "Chainlink Oracle Service"
Cohesion: 0.20
Nodes (8): oracle_price(), Fetch the latest Chainlink oracle price or market reference fallback for a…, OracleService, Any, datetime, Fetch latest price from on-chain oracle or return cached DB price., Service to query on-chain Chainlink feeds and persist price snapshots., Query Chainlink aggregator contract for latest price answer. Returns tuple of…

### Community 10 - "DeFi Protocol & TVL Metrics"
Cohesion: 0.20
Nodes (10): fetch_all_protocol_tvls(), fetch_protocol_tvl(), fetch_top_defi_protocols(), list_supported_protocols(), Any, defi_client.py — DeFi protocol data fetcher for Aegis Analytics AI. Fetches: -…, Fetch TVL for multiple DeFi protocols., Return the list of DeFi protocols supported by this client. (+2 more)

### Community 11 - "Blockchain Oracle Feeds"
Cohesion: 0.28
Nodes (8): fetch_all_oracle_prices(), fetch_chainlink_price(), get_feed_address(), _is_blockchain_enabled(), oracle_service.py — Chainlink price feed reader for Aegis Analytics AI. Reads…, Fetch latest price from a Chainlink price feed., Fetch current Chainlink prices for a list of trading pairs., Look up the Chainlink feed address for a trading pair and chain.

### Community 12 - "Linting & Code Quality (Oxlint)"
Cohesion: 0.22
Nodes (8): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, oxc, typescript, warn

### Community 13 - "Prediction & Price Anchoring"
Cohesion: 0.29
Nodes (5): Any, datetime, Hash ML prediction output and anchor hash to blockchain., Return list of anchor records for symbol., Compute price hash and anchor on-chain or store local verification record.

### Community 14 - "Blockchain Event Listener"
Cohesion: 0.29
Nodes (7): _listener_loop(), event_listener.py — Blockchain event listener for Aegis Analytics AI. Polls for…, Background polling loop. Every `poll_interval_seconds`, fetches the current…, Start the blockchain event listener as a background daemon thread. No-op if…, Signal the event listener thread to stop gracefully., start_event_listener(), stop_event_listener()

### Community 15 - "Database Migrations (Alembic)"
Cohesion: 0.32
Nodes (7): _get_url(), Alembic env.py — loads DATABASE_URL from environment at runtime., Read DATABASE_URL from environment, fall back to SQLite for local dev., Run migrations in 'offline' mode (no active DB connection required)., Run migrations in 'online' mode (active DB connection)., run_migrations_offline(), run_migrations_online()

### Community 16 - "Cryptographic Hashing & Anchor Tests"
Cohesion: 0.33
Nodes (6): compute_keccak256(), Compute sha3/keccak256 hex digest of data., fixture, test_blockchain_anchor.py — Unit tests for cryptographic hashing & anchor…, setup_test_db(), test_keccak256_computation()

### Community 17 - "Web3 Client & Oracle Tests"
Cohesion: 0.29
Nodes (5): chain_client.py — Web3 client wrapper for EVM blockchain networks (Sepolia,…, fixture, test_oracle_service.py — Unit tests for Oracle price service., setup_test_db(), test_oracle_service_fallback()

### Community 18 - "Contextual AI Assistant"
Cohesion: 0.52
Nodes (6): answer_question(), build_market_context(), evaluate_strategy(), _pct(), Any, Context-aware dashboard assistant (rule-based, uses live forecast data).

## Knowledge Gaps
- **95 isolated node(s):** `hre`, `hre`, `$schema`, `typescript`, `oxc` (+90 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 227 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Aegis Analytics System Architecture` connect `FastAPI Endpoints & Architecture` to `Frontend React UI & Components`?**
  _High betweenness centrality (0.185) - this node is a cross-community bridge._
- **Why does `ChainClient` connect `Blockchain Anchor & Web3 Client` to `FastAPI Endpoints & Architecture`, `ML Predictor & Storage Service`, `Chainlink Oracle Service`, `Blockchain Oracle Feeds`, `Blockchain Event Listener`, `Cryptographic Hashing & Anchor Tests`, `Web3 Client & Oracle Tests`, `Web3 Transaction Receipts`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Why does `init_user_store()` connect `Authentication & Streamlit Dashboard` to `FastAPI Endpoints & Architecture`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `ChainClient` (e.g. with `anchor_prediction_endpoint()` and `blockchain_anchors()`) actually correct?**
  _`ChainClient` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `hre`, `hre`, `$schema` to the rest of the system?**
  _95 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Frontend React UI & Components` be split into smaller, more focused modules?**
  _Cohesion score 0.0629746835443038 - nodes in this community are weakly interconnected._
- **Should `Authentication & Streamlit Dashboard` be split into smaller, more focused modules?**
  _Cohesion score 0.08409436834094368 - nodes in this community are weakly interconnected._