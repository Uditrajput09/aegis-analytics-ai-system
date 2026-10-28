# Graph Report - project_type_02  (2026-09-01)

## Corpus Check
- 92 files · ~89,489 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 611 nodes · 1151 edges · 55 communities (15 shown, 18 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 25 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `24791342`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- App.tsx
- app.py
- routes.py
- storage.py
- devDependencies
- train_pipeline.py
- compilerOptions
- compilerOptions
- ChainClient
- dependencies
- defi_client.py
- fetch_crypto_ohlcv
- plugins
- rules/graphify.md
- workflows/graphify.md
- env.py
- assistant.py
- deploy.js
- verify.js
- tsconfig.json
- blockchain/__init__.py
- tests/__init__.py
- Aegis System Brain & Workflow Context
- Docker Compose Orchestration (API, TimescaleDB, Streamlit)
- Project Overview (Aegis_Analytics_Project_Overview.md)
- Asset: favicon.svg
- Asset: icons.svg
- Project Overview (README.md)
- Asset: hero.png
- Asset: react.svg
- Asset: vite.svg
- Project Overview (PROJECT.md)
- Project Overview (README.md)

## God Nodes (most connected - your core abstractions)
1. `main()` - 40 edges
2. `ChainClient` - 28 edges
3. `react` - 21 edges
4. `compilerOptions` - 18 edges
5. `load_settings()` - 17 edges
6. `predict_latest()` - 16 edges
7. `apiService` - 16 edges
8. `horizon_label()` - 15 edges
9. `compilerOptions` - 15 edges
10. `_make_engine()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `auth_login()` --calls--> `authenticate_user()`  [EXTRACTED]
  backend/app/api/routes.py → dashboard/user_store.py
- `auth_login()` --calls--> `get_or_create_demo_user()`  [EXTRACTED]
  backend/app/api/routes.py → dashboard/user_store.py
- `auth_login()` --calls--> `init_user_store()`  [EXTRACTED]
  backend/app/api/routes.py → dashboard/user_store.py
- `auth_register()` --calls--> `init_user_store()`  [EXTRACTED]
  backend/app/api/routes.py → dashboard/user_store.py
- `auth_register()` --calls--> `register_user()`  [EXTRACTED]
  backend/app/api/routes.py → dashboard/user_store.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Dual-Head LightGBM Forecasting & Conformal Risk Pipeline** — backend_app_services_predictor [INFERRED 0.95]

## Communities (55 total, 18 thin omitted)

### Community 0 - "App.tsx"
Cohesion: 0.05
Nodes (69): App(), BrandLogo(), BrandLogoProps, FinancialVisualization(), HeroSection(), LoginCard(), LoginCardProps, AppLayout() (+61 more)

### Community 1 - "app.py"
Cohesion: 0.08
Nodes (69): auth_login(), auth_register(), AuthRequest, BaseModel, Connection, add_indicators(), api_ok(), build_advice() (+61 more)

### Community 2 - "routes.py"
Cohesion: 0.06
Nodes (70): Aegis Analytics System Architecture, anchor_prediction_endpoint(), bars_recent(), blockchain_status(), crypto_bars_recent(), crypto_symbols(), defi_global(), defi_protocols() (+62 more)

### Community 3 - "storage.py"
Cohesion: 0.06
Nodes (62): blockchain_verify(), Look up an anchor record by its transaction hash and return verification status., fetch_chainlink_price(), get_feed_address(), _is_blockchain_enabled(), OracleService, Any, datetime (+54 more)

### Community 4 - "devDependencies"
Cohesion: 0.06
Nodes (32): autoprefixer, devDependencies, autoprefixer, oxlint, postcss, tailwindcss, @tailwindcss/postcss, @types/node (+24 more)

### Community 5 - "train_pipeline.py"
Cohesion: 0.11
Nodes (26): add_time_features(), _base_price_features(), build_features_and_targets(), build_latest_features(), _cyclical_features(), horizons_from_config(), HorizonSpec, DataFrame (+18 more)

### Community 6 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 7 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 8 - "ChainClient"
Cohesion: 0.06
Nodes (37): blockchain_anchors(), List on-chain anchor records for a given symbol., AnchorService, compute_keccak256(), Any, datetime, anchor_service.py — Cryptographic hashing and on-chain anchoring service.…, Hash ML prediction output and anchor hash to blockchain. (+29 more)

### Community 9 - "dependencies"
Cohesion: 0.06
Nodes (33): clsx, d3, d3-drag, d3-force, d3-selection, d3-zoom, dependencies, clsx (+25 more)

### Community 10 - "defi_client.py"
Cohesion: 0.20
Nodes (10): fetch_all_protocol_tvls(), fetch_protocol_tvl(), fetch_top_defi_protocols(), list_supported_protocols(), Any, defi_client.py — DeFi protocol data fetcher for Aegis Analytics AI. Fetches: -…, Fetch TVL for multiple DeFi protocols., Return the list of DeFi protocols supported by this client. (+2 more)

### Community 11 - "fetch_crypto_ohlcv"
Cohesion: 0.36
Nodes (7): _fetch_coingecko_ohlcv(), fetch_crypto_ohlcv(), DataFrame, datetime, crypto_client.py — Binance & CoinGecko OHLCV data fetcher for Aegis Analytics…, Fallback: fetch daily OHLCV from CoinGecko public REST API., Fetch OHLCV candlestick data directly from Binance public REST API. Does not…

### Community 12 - "plugins"
Cohesion: 0.22
Nodes (8): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, oxc, typescript, warn

### Community 15 - "env.py"
Cohesion: 0.32
Nodes (7): _get_url(), Alembic env.py — loads DATABASE_URL from environment at runtime., Read DATABASE_URL from environment, fall back to SQLite for local dev., Run migrations in 'offline' mode (no active DB connection required)., Run migrations in 'online' mode (active DB connection)., run_migrations_offline(), run_migrations_online()

### Community 18 - "assistant.py"
Cohesion: 0.52
Nodes (6): answer_question(), build_market_context(), evaluate_strategy(), _pct(), Any, Context-aware dashboard assistant (rule-based, uses live forecast data).

## Knowledge Gaps
- **112 isolated node(s):** `hre`, `hre`, `$schema`, `typescript`, `oxc` (+107 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 248 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Aegis Analytics System Architecture` connect `routes.py` to `App.tsx`?**
  _High betweenness centrality (0.187) - this node is a cross-community bridge._
- **Why does `ChainClient` connect `ChainClient` to `routes.py`, `storage.py`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Why does `init_user_store()` connect `app.py` to `routes.py`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `ChainClient` (e.g. with `anchor_prediction_endpoint()` and `blockchain_anchors()`) actually correct?**
  _`ChainClient` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `hre`, `hre`, `$schema` to the rest of the system?**
  _112 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `App.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.05236091631603553 - nodes in this community are weakly interconnected._
- **Should `app.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08409436834094368 - nodes in this community are weakly interconnected._