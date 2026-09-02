# Aegis Analytics AI — Frontend Web Application

A modern, high-performance financial intelligence single-page application (SPA) built with **React 19**, **TypeScript 6**, **Vite 8**, and **Tailwind CSS v4**.

---

## ⚡ Tech Stack & Tooling

| Category | Technology | Description |
| :--- | :--- | :--- |
| **Framework** | [React 19](https://react.dev/) (`^19.2.8`) | Latest React concurrent architecture with declarative component trees |
| **Type System** | [TypeScript](https://www.typescriptlang.org/) (`~6.0.2`) | Strict type-safety across API contracts, charts, and state models |
| **Build Tool** | [Vite 8](https://vitejs.dev/) (`^8.2.0`) | Lightning-fast ESM build tool & Hot Module Replacement (HMR) |
| **Styling** | [Tailwind CSS v4](https://tailwindcss.com/) (`^4.3.3`) | Next-gen CSS-first configuration via `@tailwindcss/postcss` & PostCSS 8 |
| **Charts & Telemetry** | [Recharts](https://recharts.org/) (`^3.10.1`) | Composable responsive SVG charts (candlesticks, area, line, bar, risk gauges) |
| **Icons** | [Lucide React](https://lucide.dev/) (`^1.31.0`) | Feather-derived minimalist icon system |
| **Linter & Quality** | [Oxlint](https://oxc.rs/) (`^1.75.0`) | High-speed Rust-based linter |
| **Styling Utilities** | `clsx` (`^2.1.1`), `tailwind-merge` (`^3.6.0`) | Dynamic and conflict-free className resolution |

---

## 🖥️ Application Pages & Modules

The frontend provides 12 specialized pages located in [`src/pages/`](file:///c:/Users/Asus/Desktop/project_type_02/frontend/src/pages):

```
frontend/src/pages/
├── OverviewPage.tsx          # Multi-asset executive telemetry, index trackers & live forecasts
├── MarketAnalyticsPage.tsx   # Interactive price charts, volume profiling & technical indicators
├── ForecastsPage.tsx         # Dual-head ML returns, directional confidence (p_up) & conformal intervals
├── RiskAnalyticsPage.tsx     # Downside tail risk, VaR / CVaR metrics & uncertainty distributions
├── CryptoDefiPage.tsx        # Binance / CoinGecko market streaming & DeFiLlama TVL analytics
├── AIAnalystPage.tsx         # Autonomous quantitative conversational assistant & trade signals
├── BlockchainAuditPage.tsx   # On-chain cryptographic prediction anchoring & audit verifier
├── InsightsPage.tsx          # Macroeconomic sentiment, quantitative momentum & factor scoring
├── ReportsPage.tsx           # Automated financial intelligence export & audit trail generator
├── WatchlistPage.tsx         # Custom user equity & crypto portfolio watchlists with alerts
├── SettingsPage.tsx          # RPC node configuration, API keys, ML hyperparameters & preferences
└── LoginPage.tsx             # Glassmorphic user authentication & demo preset credentials
```

### Page Capabilities Breakdown

1. **[OverviewPage.tsx](file:///c:/Users/Asus/Desktop/project_type_02/frontend/src/pages/OverviewPage.tsx)**: Executive dashboard showing live market pulse, active predictions, model confidence gauges, top movers, and quick navigation.
2. **[MarketAnalyticsPage.tsx](file:///c:/Users/Asus/Desktop/project_type_02/frontend/src/pages/MarketAnalyticsPage.tsx)**: Deep technical charting with multi-timeframe OHLCV bars (`1m`, `5m`, `15m`, `1h`, `1d`), moving averages ($MA_{20}$, $MA_{50}$, $MA_{200}$), RSI, and MACD.
3. **[ForecastsPage.tsx](file:///c:/Users/Asus/Desktop/project_type_02/frontend/src/pages/ForecastsPage.tsx)**: Real-time dual-head LightGBM predictions, expected future prices, calibrated directional confidence ($p_{\text{up}}$), and finite-sample $(1-\alpha)$ conformal prediction bounds.
4. **[RiskAnalyticsPage.tsx](file:///c:/Users/Asus/Desktop/project_type_02/frontend/src/pages/RiskAnalyticsPage.tsx)**: Statistical risk quantification displaying tail-event probabilities ($P(\text{Return} < -1\%)$ and $P(\text{Return} < -2\%)$), Value-at-Risk, and volatility bands.
5. **[CryptoDefiPage.tsx](file:///c:/Users/Asus/Desktop/project_type_02/frontend/src/pages/CryptoDefiPage.tsx)**: Live crypto price action via Binance / CoinGecko APIs and DeFi protocol metrics (Total Value Locked via DeFiLlama, top Uniswap V3 liquidity pools via The Graph).
6. **[AIAnalystPage.tsx](file:///c:/Users/Asus/Desktop/project_type_02/frontend/src/pages/AIAnalystPage.tsx)**: Quantitative market intelligence assistant answering complex asset queries, signal breakdowns, and risk assessments.
7. **[BlockchainAuditPage.tsx](file:///c:/Users/Asus/Desktop/project_type_02/frontend/src/pages/BlockchainAuditPage.tsx)**: Web3 verification explorer allowing users to inspect immutable on-chain price and prediction anchors with Etherscan / Polygonscan block explorer links.
8. **[InsightsPage.tsx](file:///c:/Users/Asus/Desktop/project_type_02/frontend/src/pages/InsightsPage.tsx)**: Quantitative factor attribution, momentum indicators, and market regime classification.
9. **[ReportsPage.tsx](file:///c:/Users/Asus/Desktop/project_type_02/frontend/src/pages/ReportsPage.tsx)**: Automated audit trail report generation, performance summaries, and export tools.
10. **[WatchlistPage.tsx](file:///c:/Users/Asus/Desktop/project_type_02/frontend/src/pages/WatchlistPage.tsx)**: Persistent custom asset watchlists with custom price target alerts.
11. **[SettingsPage.tsx](file:///c:/Users/Asus/Desktop/project_type_02/frontend/src/pages/SettingsPage.tsx)**: Configure Web3 RPC endpoints, API credentials (Binance, CoinGecko, Infura), and interface preferences.
12. **[LoginPage.tsx](file:///c:/Users/Asus/Desktop/project_type_02/frontend/src/pages/LoginPage.tsx)**: Premium glassmorphism authentication with session tokens and one-click demo login.

---

## 🏛️ Component Architecture & Layout

```
frontend/src/
├── assets/                   # Static SVG assets & brand icons
├── components/
│   └── auth/                 # BrandLogo, FinancialVisualization & auth cards
├── layouts/
│   └── AppLayout.tsx         # Unified responsive shell with sidebar navigation & topbar status
├── pages/                    # 12 application view pages
├── services/
│   └── api.ts                # Centralized typed HTTP client communicating with FastAPI backend
├── types/
│   └── api.ts                # TypeScript data interfaces for bars, predictions, risk, and anchors
├── App.css                   # Global layout animations & scrollbar utilities
├── App.tsx                   # Main router & active view switcher
├── index.css                 # Tailwind CSS v4 directives & theme tokens
└── main.tsx                  # Application entry point & DOM root mounting
```

---

## 🚀 Getting Started (Development & Build)

### Prerequisites
- Node.js 18+ (Node 20+ recommended)
- npm or yarn / pnpm

### Installation
From the `frontend/` directory:
```bash
npm install
```

### Running the Development Server
```bash
npm run dev
```
The application will launch on `http://localhost:5173`. Ensure the FastAPI backend server is running on `http://127.0.0.1:8000`.

### Typecheck & Production Build
```bash
npm run build
```

### Linting
```bash
npm run lint
```

### Local Preview of Production Build
```bash
npm run preview
```

---

## 🔗 Backend API Integration

All frontend API calls are routed through [`src/services/api.ts`](file:///c:/Users/Asus/Desktop/project_type_02/frontend/src/services/api.ts), which targets the FastAPI REST backend:

- Base URL: `http://127.0.0.1:8000` (or configured via environment)
- Endpoints consumed:
  - `/bars/recent` — OHLCV historical price series
  - `/predictions/latest` — ML expected returns, expected price, $p_{\text{up}}$, and conformal bounds
  - `/risk/latest` — Downside tail-risk probabilities
  - `/blockchain/anchors/{symbol}` — On-chain smart contract anchor history
  - `/blockchain/verify/{tx_hash}` — Transaction hash cryptographic verification
  - `/blockchain/status` — Web3 connection & smart contract address state
  - `/oracle/prices/{pair}` — Chainlink decentralized oracle prices
  - `/crypto/symbols` & `/crypto/bars/recent` — Binance / CoinGecko crypto data
  - `/defi/tvl/{protocol}` & `/defi/uniswap/pools` — DeFiLlama & Uniswap V3 metrics
  - `/auth/login` & `/auth/register` — User authentication
