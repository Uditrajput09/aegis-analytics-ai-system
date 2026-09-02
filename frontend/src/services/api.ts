import type {
  HealthResponse,
  SymbolListResponse,
  BarsResponse,
  PredictionLatest,
  RiskLatest,
  AIInsight,
  User,
  AuthResponse,
  BlockchainAnchor,
  OraclePriceResponse,
  CryptoBarsResponse,
  DefiProtocol,
} from '../types/api';

const getBaseUrl = (): string => {
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }
  // Default to backend on 127.0.0.1:8000 when served on localhost dev port 3000
  if (typeof window !== 'undefined' && window.location.hostname === 'localhost') {
    return 'http://127.0.0.1:8000';
  }
  return 'http://127.0.0.1:8000';
};

const API_BASE_URL = getBaseUrl();

class ApiError extends Error {
  status?: number;
  constructor(message: string, status?: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

async function fetchJson<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  try {
    const res = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(options?.headers || {}),
      },
    });

    if (!res.ok) {
      const errorText = await res.text();
      let errorDetail = errorText;
      try {
        const jsonErr = JSON.parse(errorText);
        errorDetail = jsonErr.detail || errorText;
      } catch {
        // fallback to raw text
      }
      throw new ApiError(errorDetail || `HTTP error ${res.status}`, res.status);
    }

    return (await res.json()) as T;
  } catch (err: any) {
    if (err instanceof ApiError) {
      throw err;
    }
    throw new ApiError(err.message || 'Failed to connect to Aegis backend service', 0);
  }
}

export const apiService = {
  getApiBaseUrl(): string {
    return API_BASE_URL;
  },

  getStoredUser(): User | null {
    try {
      const raw = localStorage.getItem('aegis_user');
      return raw ? (JSON.parse(raw) as User) : null;
    } catch {
      return null;
    }
  },

  setStoredUser(user: User, token: string): void {
    localStorage.setItem('aegis_user', JSON.stringify(user));
    localStorage.setItem('aegis_token', token);
  },

  clearStoredUser(): void {
    localStorage.removeItem('aegis_user');
    localStorage.removeItem('aegis_token');
  },

  async login(username: string, password: string): Promise<AuthResponse> {
    const res = await fetchJson<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    if (res && res.user && res.token) {
      this.setStoredUser(res.user, res.token);
    }
    return res;
  },

  async register(username: string, password: string): Promise<{ ok: boolean; message: string }> {
    return fetchJson<{ ok: boolean; message: string }>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  },

  async getHealth(): Promise<HealthResponse> {
    return fetchJson<HealthResponse>('/health');
  },

  async getSymbols(): Promise<string[]> {
    const data = await fetchJson<SymbolListResponse>('/meta/symbols');
    return data.symbols || [];
  },

  async getRecentBars(symbol: string, timeframe: string = '1m', limit: number = 300): Promise<BarsResponse> {
    const params = new URLSearchParams({
      symbol: symbol.toUpperCase(),
      timeframe,
      limit: limit.toString(),
    });
    return fetchJson<BarsResponse>(`/bars/recent?${params.toString()}`);
  },

  async getLatestPrediction(
    symbol: string,
    horizon: string = '5m',
    timeframe?: string,
    forceUpdate: boolean = false
  ): Promise<PredictionLatest> {
    const params = new URLSearchParams({
      symbol: symbol.toUpperCase(),
      horizon,
      force_update: forceUpdate ? 'true' : 'false',
    });
    if (timeframe) {
      params.append('timeframe', timeframe);
    }
    return fetchJson<PredictionLatest>(`/predictions/latest?${params.toString()}`);
  },

  async getLatestRisk(
    symbol: string,
    horizon: string = '5m',
    timeframe?: string,
    forceUpdate: boolean = false
  ): Promise<RiskLatest> {
    const params = new URLSearchParams({
      symbol: symbol.toUpperCase(),
      horizon,
      force_update: forceUpdate ? 'true' : 'false',
    });
    if (timeframe) {
      params.append('timeframe', timeframe);
    }
    return fetchJson<RiskLatest>(`/risk/latest?${params.toString()}`);
  },

  async getMultiHorizonPredictions(symbol: string): Promise<Record<string, PredictionLatest>> {
    const horizons = [
      { horizon: '5m', timeframe: '1m' },
      { horizon: '15m', timeframe: '1m' },
      { horizon: '60m', timeframe: '1m' },
      { horizon: '1d', timeframe: '1d' },
    ];

    const results: Record<string, PredictionLatest> = {};
    const promises = horizons.map(async ({ horizon, timeframe }) => {
      try {
        const pred = await this.getLatestPrediction(symbol, horizon, timeframe);
        results[horizon] = pred;
      } catch (err) {
        console.warn(`Failed to fetch forecast for ${horizon}:`, err);
      }
    });

    await Promise.all(promises);
    return results;
  },

  deriveSignal(pred: PredictionLatest, risk: RiskLatest): { label: string; color: string; reason: string } {
    const expRet = pred.expected_return;
    const pUp = pred.p_up;
    const pDown2 = risk.p_return_below_minus_2pct;

    if (expRet > 0.002 && (pUp === null || pUp > 0.60) && pDown2 < 0.20) {
      return {
        label: 'Strong Buy',
        color: 'text-aegis-positive bg-emerald-500/10 border-emerald-500/30',
        reason: 'Positive expected return with high directional confidence and minimal tail risk.',
      };
    } else if (expRet > 0 && pDown2 < 0.35) {
      return {
        label: 'Cautious Hold',
        color: 'text-amber-400 bg-amber-500/10 border-amber-500/30',
        reason: 'Slight positive return estimate, but prediction interval shows moderate variance.',
      };
    } else if (expRet <= 0 && (pUp !== null && pUp < 0.40)) {
      return {
        label: 'Sell / Reduce',
        color: 'text-aegis-risk bg-red-500/10 border-red-500/30',
        reason: 'Negative expected return and weak directional momentum detected across models.',
      };
    }
    return {
      label: 'Neutral / Hold',
      color: 'text-slate-300 bg-slate-500/10 border-slate-500/30',
      reason: 'Model output is balanced near zero return with normal variance bounds.',
    };
  },

  deriveAIInsights(pred: PredictionLatest, risk: RiskLatest): AIInsight[] {
    const expRetPct = (pred.expected_return * 100).toFixed(2);
    const pUpPct = pred.p_up ? (pred.p_up * 100).toFixed(1) : null;
    const lowPct = (pred.interval_low * 100).toFixed(2);
    const highPct = (pred.interval_high * 100).toFixed(2);
    const pDown1 = (risk.p_return_below_minus_1pct * 100).toFixed(1);
    const pDown2 = (risk.p_return_below_minus_2pct * 100).toFixed(1);

    const insights: AIInsight[] = [];

    // Opportunity
    if (pred.expected_return > 0) {
      insights.push({
        id: '1',
        category: 'OPPORTUNITY',
        title: 'Positive Return Expectation',
        description: `LightGBM regressor projects a ${expRetPct}% expected return over the ${pred.horizon} horizon, targeting ₹${pred.expected_price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}.`,
        impact: 'POSITIVE',
        metric: 'Expected Return',
        value: `+${expRetPct}%`,
      });
    } else {
      insights.push({
        id: '1',
        category: 'RECOMMENDATION',
        title: 'Neutral / Bearish Outlook',
        description: `Expected return is negative or flat (${expRetPct}%). Consider waiting for improved probability alignment before entry.`,
        impact: 'NEUTRAL',
        metric: 'Expected Return',
        value: `${expRetPct}%`,
      });
    }

    // Risk
    if (risk.p_return_below_minus_2pct > 0.15) {
      insights.push({
        id: '2',
        category: 'RISK DETECTED',
        title: 'Elevated Downside Risk',
        description: `Conformal bounds indicate a ${pDown2}% probability of return dropping below -2% and ${pDown1}% probability of dropping below -1%.`,
        impact: 'CRITICAL',
        metric: 'P(Return < -2%)',
        value: `${pDown2}%`,
      });
    } else {
      insights.push({
        id: '2',
        category: 'RISK DETECTED',
        title: 'Controlled Downside Tail',
        description: `Downside risk remains contained with only ${pDown1}% probability of a >1% drawdown within this horizon.`,
        impact: 'NEUTRAL',
        metric: 'P(Return < -1%)',
        value: `${pDown1}%`,
      });
    }

    // Trend
    if (pUpPct) {
      insights.push({
        id: '3',
        category: 'TREND',
        title: 'Isotonic Calibrated Confidence',
        description: `Directional classification calibrator estimates a ${pUpPct}% probability of upward price movement.`,
        impact: parseFloat(pUpPct) > 55 ? 'POSITIVE' : parseFloat(pUpPct) < 45 ? 'CRITICAL' : 'NEUTRAL',
        metric: 'P(Up)',
        value: `${pUpPct}%`,
      });
    }

    // Recommendation
    insights.push({
      id: '4',
      category: 'RECOMMENDATION',
      title: 'Conformal Interval Coverage (90%)',
      description: `Model distribution bounds guarantee 90% statistical coverage between ${lowPct}% and +${highPct}%. Review bounds before sizing positions.`,
      impact: 'NEUTRAL',
      metric: 'Prediction Band',
      value: `${lowPct}% to +${highPct}%`,
    });

    return insights;
  },

  async getBlockchainAnchors(symbol: string, limit: number = 50): Promise<BlockchainAnchor[]> {
    const res = await fetchJson<{ symbol: string; anchors: BlockchainAnchor[] }>(
      `/blockchain/anchors/${encodeURIComponent(symbol.toUpperCase())}?limit=${limit}`
    );
    return res.anchors || [];
  },

  async anchorPrediction(symbol: string, horizon: string = '5m', timeframe: string = '1m'): Promise<any> {
    const params = new URLSearchParams({
      symbol: symbol.toUpperCase(),
      horizon,
      timeframe,
    });
    return fetchJson(`/blockchain/anchor-prediction?${params.toString()}`, { method: 'POST' });
  },

  async getOraclePrice(symbol: string): Promise<OraclePriceResponse> {
    return fetchJson<OraclePriceResponse>(`/oracle/prices/${encodeURIComponent(symbol.toUpperCase())}`);
  },

  async getCryptoBars(symbol: string = 'BTCUSDT', interval: string = '1m', limit: number = 300): Promise<CryptoBarsResponse> {
    const params = new URLSearchParams({
      symbol: symbol.toUpperCase(),
      interval,
      limit: limit.toString(),
    });
    return fetchJson<CryptoBarsResponse>(`/crypto/bars/recent?${params.toString()}`);
  },

  async getTopDefiProtocols(limit: number = 10): Promise<DefiProtocol[]> {
    const res = await fetchJson<{ count: number; protocols: DefiProtocol[] }>(`/defi/top?limit=${limit}`);
    return res.protocols || [];
  },
};

