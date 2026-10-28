# Graph Report - project_type_02  (2026-10-28)

## Corpus Check
- 109 files · ~204,668 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 861 nodes · 1638 edges · 74 communities (33 shown, 19 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 40 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7bc8598f`
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
- oracle_service.py
- plugins
- rules/graphify.md
- workflows/graphify.md
- env.py
- 💼 PART 2 — BUSINESS QUESTIONS (Q51–Q100)
- AnchorService
- Db2ConnectionManager
- MODEL_EVALUATION_REPORT.md
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
- .anchor_prediction
- event_listener.py
- db2_toolkit/__init__.py
- db2_routes.py
- test_db2_toolkit.py
- .get_connection
- MockDb2Sandbox
- Db2TextToSqlAgent
- 🏛️ IBM Db2 AI & Analytics Toolkit — Master Implementation Plan
- .execute_query
- Db2Config
- haystack_pipeline.py
- .transpile
- ._build_default_pipeline
- .export_flow_dict
- .run_qa

## God Nodes (most connected - your core abstractions)
1. `main()` - 40 edges
2. `Db2ConnectionManager` - 39 edges
3. `ChainClient` - 28 edges
4. `get_db2_pool()` - 22 edges
5. `react` - 20 edges
6. `compilerOptions` - 18 edges
7. `load_settings()` - 17 edges
8. `predict_latest()` - 16 edges
9. `horizon_label()` - 15 edges
10. `MockDb2Sandbox` - 15 edges

## Surprising Connections (you probably didn't know these)
- `get_db2_schema()` --uses--> `Db2TextToSqlAgent`  [INFERRED]
  backend/app/api/db2_routes.py → db2_toolkit/langchain_agent.py
- `transpile_sql()` --uses--> `Db2DialectTranspiler`  [INFERRED]
  backend/app/api/db2_routes.py → db2_toolkit/dialect_transpiler.py
- `execute_query()` --uses--> `Db2DialectTranspiler`  [INFERRED]
  backend/app/api/db2_routes.py → db2_toolkit/dialect_transpiler.py
- `execute_query()` --uses--> `Db2TextToSqlAgent`  [INFERRED]
  backend/app/api/db2_routes.py → db2_toolkit/langchain_agent.py
- `search_rag_documents()` --uses--> `Db2VectorStore`  [INFERRED]
  backend/app/api/db2_routes.py → db2_toolkit/langchain_agent.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Dual-Head LightGBM Forecasting & Conformal Risk Pipeline** — backend_app_services_predictor [INFERRED 0.95]

## Communities (74 total, 19 thin omitted)

### Community 0 - "App.tsx"
Cohesion: 0.06
Nodes (57): App(), BrandLogo(), BrandLogoProps, FinancialVisualization(), HeroSection(), LoginCard(), LoginCardProps, AppLayout() (+49 more)

### Community 1 - "app.py"
Cohesion: 0.07
Nodes (75): auth_login(), auth_register(), AuthRequest, BaseModel, post, Connection, add_indicators(), api_ok() (+67 more)

### Community 2 - "routes.py"
Cohesion: 0.05
Nodes (68): Aegis Analytics System Architecture, anchor_prediction_endpoint(), bars_recent(), blockchain_anchors(), blockchain_status(), crypto_bars_recent(), crypto_symbols(), defi_global() (+60 more)

### Community 3 - "storage.py"
Cohesion: 0.06
Nodes (62): blockchain_verify(), Look up an anchor record by its transaction hash and return verification status., _artifact_path(), _ensure_minimum_bars(), _load_artifact(), predict_latest(), PredictionOut, DataFrame (+54 more)

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
Cohesion: 0.12
Nodes (9): ChainClient, Any, Wrapper around Web3 instance with safe connection handling and transaction…, Return True if Web3 connection to RPC node is active., Fetch current block height on target chain., Fetch current gas price in wei., Get ETH/MATIC balance for an address., Broadcast a pre-signed raw transaction to the network. (+1 more)

### Community 9 - "dependencies"
Cohesion: 0.06
Nodes (33): clsx, d3, d3-drag, d3-force, d3-selection, d3-zoom, dependencies, clsx (+25 more)

### Community 10 - "defi_client.py"
Cohesion: 0.22
Nodes (8): fetch_all_protocol_tvls(), fetch_top_defi_protocols(), list_supported_protocols(), Any, defi_client.py — DeFi protocol data fetcher for Aegis Analytics AI. Fetches: -…, Fetch TVL for multiple DeFi protocols., Return the list of DeFi protocols supported by this client., Fetch top DeFi protocols by TVL from DeFiLlama API.

### Community 11 - "oracle_service.py"
Cohesion: 0.15
Nodes (14): fetch_all_oracle_prices(), fetch_chainlink_price(), get_feed_address(), _is_blockchain_enabled(), OracleService, Any, datetime, oracle_service.py — Chainlink price feed reader for Aegis Analytics AI. Reads… (+6 more)

### Community 12 - "plugins"
Cohesion: 0.22
Nodes (8): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, oxc, typescript, warn

### Community 15 - "env.py"
Cohesion: 0.32
Nodes (7): _get_url(), Alembic env.py — loads DATABASE_URL from environment at runtime., Read DATABASE_URL from environment, fall back to SQLite for local dev., Run migrations in 'offline' mode (no active DB connection required)., Run migrations in 'online' mode (active DB connection)., run_migrations_offline(), run_migrations_online()

### Community 16 - "💼 PART 2 — BUSINESS QUESTIONS (Q51–Q100)"
Cohesion: 0.12
Nodes (16): 🏆 Aegis Analytics AI — 100 Hackathon Questions & Answers, 🔹 Architecture & System Design, 🔹 Blockchain & Web3, 🔹 Competitive Landscape, 🔹 Feature Engineering, 🔹 Financial Performance & Metrics, 🔹 Frontend & Infrastructure, 🔹 Innovation, Ethics & Risk (+8 more)

### Community 17 - "AnchorService"
Cohesion: 0.21
Nodes (9): AnchorService, anchor_service.py — Cryptographic hashing and on-chain anchoring service.…, Service to anchor prices and predictions on-chain and record audit trails., chain_client.py — Web3 client wrapper for EVM blockchain networks (Sepolia,…, fixture, test_blockchain_anchor.py — Unit tests for cryptographic hashing & anchor…, setup_test_db(), test_anchor_prediction() (+1 more)

### Community 18 - "Db2ConnectionManager"
Cohesion: 0.10
Nodes (21): Db2ConnectionManager, get_db2_pool(), IBM Db2 Connection Manager and Connection Pooling. Handles thread-safe…, Returns singleton Db2ConnectionManager instance., Thread-safe Connection Manager for IBM Db2 with Mock Sandbox Fallback., Whether current manager operates against the mock engine., AgentMessage, Db2Crew (+13 more)

### Community 19 - "MODEL_EVALUATION_REPORT.md"
Cohesion: 0.17
Nodes (11): 1. Ready-to-Paste Slide Content (for PPT), 2. Multi-Asset Comparative Summary Table, 3. Calibration Chart Data (Predicted Confidence vs. Actual Realized Frequency), 4. Visual Calibration Reliability Diagram, 5. Generated Chart Media Files, 6. Executive Talking Points & Methodology Notes, A. 5-Bin Quintile Table (Recommended for Slide Decks), B. 10-Bin Decile Table (Institutional / Academic Standard) (+3 more)

### Community 58 - ".anchor_prediction"
Cohesion: 0.22
Nodes (8): compute_keccak256(), Any, datetime, Hash ML prediction output and anchor hash to blockchain., Return list of anchor records for symbol., Compute sha3/keccak256 hex digest of data., Compute price hash and anchor on-chain or store local verification record., test_keccak256_computation()

### Community 59 - "event_listener.py"
Cohesion: 0.29
Nodes (7): _listener_loop(), event_listener.py — Blockchain event listener for Aegis Analytics AI. Polls for…, Background polling loop. Every `poll_interval_seconds`, fetches the current…, Start the blockchain event listener as a background daemon thread. No-op if…, Signal the event listener thread to stop gracefully., start_event_listener(), stop_event_listener()

### Community 60 - "db2_toolkit/__init__.py"
Cohesion: 0.13
Nodes (16): Executes a SQL query against IBM Db2., Db2DialectTranspiler, IBM Db2 SQLGlot Dialect and Cross-Dialect Transpiler. Translates queries from…, Convenience helper translating SQL directly to Db2 syntax., Translates SQL expressions into IBM Db2 LUW compliant syntax., transpile_to_db2(), IBM Db2 AI & Analytics Toolkit for Aegis Analytics AI., Db2VectorStore (+8 more)

### Community 61 - "db2_routes.py"
Cohesion: 0.17
Nodes (25): CrewAuditRequest, execute_query(), export_langflow_template(), get_db2_health(), get_db2_schema(), Any, BaseModel, get (+17 more)

### Community 62 - "test_db2_toolkit.py"
Cohesion: 0.10
Nodes (27): get_db2_config(), Returns a cached Db2 configuration instance., Db2HaystackPipeline, Orchestrates an end-to-end Haystack 2.x pipeline over IBM Db2., Db2LangflowBuilder, Langflow IBM Db2 Extension Components and Flow Exporter (lfx-ibm). Provides…, Builds and serializes IBM Db2 visual flows into standard Langflow JSON., Db2LlamaIndexVectorStore (+19 more)

### Community 63 - ".get_connection"
Cohesion: 0.15
Nodes (9): Any, Context manager yielding a healthy connection with automatic release., Executes a SELECT query with retry logic and returns list of dict records., Executes a DDL or DML statement (INSERT, UPDATE, DELETE) and returns affected…, Provides an atomic transaction block with commit/rollback., Health check verifying database responsiveness., Describes columns and data types for a given table., Acquires a raw connection from the pool or opens a new one. (+1 more)

### Community 64 - "MockDb2Sandbox"
Cohesion: 0.20
Nodes (6): Returns the underlying mock sandbox instance if in mock mode., MockDb2Sandbox, Mock IBM Db2 LUW Sandbox Engine. Provides an offline, high-fidelity in-memory…, In-memory mock database simulating IBM Db2 LUW., Describes column names and types for a given table., Initializes default tables and sample market/risk data.

### Community 65 - "Db2TextToSqlAgent"
Cohesion: 0.25
Nodes (6): Db2TextToSqlAgent, Any, Natural Language Text-to-SQL Agent for IBM Db2 LUW., Inspects all tables and column types available in the database., Translates natural language intent into valid IBM Db2 SQL., Runs the complete Text-to-SQL pipeline: generation, execution, and synthesis.

### Community 66 - "🏛️ IBM Db2 AI & Analytics Toolkit — Master Implementation Plan"
Cohesion: 0.13
Nodes (14): 1. Executive Summary, 2. Complete Toolkit Component Breakdown, 3. End-to-End System Architecture, 4. Target Directory & File Structure, 5. Phase-by-Phase Implementation Plan, 6. Connection & Environment Configuration, 7. Verification & Smoke Testing Strategy, 🏛️ IBM Db2 AI & Analytics Toolkit — Master Implementation Plan (+6 more)

### Community 67 - ".execute_query"
Cohesion: 0.22
Nodes (5): Any, Returns all table names in this mock catalog., Executes a SELECT query against the mock sandbox., Executes INSERT / UPDATE / DELETE statement., Simulates IBM Db2 Visual Explain plan operator graph.

### Community 68 - "Db2Config"
Cohesion: 0.14
Nodes (9): BaseSettings, Db2Config, BaseModel, IBM Db2 Configuration and Environment Parser for Aegis Analytics AI., IBM Db2 Typed Settings., Constructs the native ibm_db connection string., Constructs the SQLAlchemy connection URL., Fallback Db2 settings without pydantic-settings. (+1 more)

### Community 69 - "haystack_pipeline.py"
Cohesion: 0.13
Nodes (15): Db2DocumentStore, Db2EmbeddingRetriever, HaystackDocument, Deepset Haystack 2.x Integration for IBM Db2 (ibm-db-haystack). Implements…, Haystack 2.x Retriever retrieving documents from Db2DocumentStore., Retrieves top-k closest documents to the query string., Document representation compatible with Haystack 2.x., Haystack 2.x Document Store backed by IBM Db2 LUW. (+7 more)

### Community 70 - ".transpile"
Cohesion: 0.50
Nodes (3): Result of cross-dialect SQL transpilation to IBM Db2., Translates a source SQL string into IBM Db2 syntax., TranspileResult

### Community 73 - "._build_default_pipeline"
Cohesion: 0.29
Nodes (5): FlowEdge, FlowNode, Represents a visual Langflow graph node., Represents a directed link between nodes in a Langflow graph., Constructs default multi-stage Db2 workflow.

### Community 74 - ".export_flow_dict"
Cohesion: 0.40
Nodes (3): Any, Exports graph structure as a standard Langflow dictionary., Serializes flow dictionary into formatted JSON string.

## Knowledge Gaps
- **141 isolated node(s):** `hre`, `hre`, `$schema`, `typescript`, `oxc` (+136 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 373 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Aegis Analytics System Architecture` connect `routes.py` to `App.tsx`?**
  _High betweenness centrality (0.135) - this node is a cross-community bridge._
- **Why does `ChainClient` connect `ChainClient` to `routes.py`, `storage.py`, `oracle_service.py`, `AnchorService`, `event_listener.py`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `Db2ConnectionManager` connect `Db2ConnectionManager` to `MockDb2Sandbox`, `Db2TextToSqlAgent`, `Db2Config`, `haystack_pipeline.py`, `db2_toolkit/__init__.py`, `test_db2_toolkit.py`, `.get_connection`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Db2ConnectionManager` (e.g. with `MockDb2Sandbox` and `Db2Crew`) actually correct?**
  _`Db2ConnectionManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `ChainClient` (e.g. with `anchor_prediction_endpoint()` and `blockchain_anchors()`) actually correct?**
  _`ChainClient` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `hre`, `hre`, `$schema` to the rest of the system?**
  _141 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `App.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.0629746835443038 - nodes in this community are weakly interconnected._