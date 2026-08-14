export interface PredictionLatest {
  symbol: string;
  horizon: string;
  timeframe: string;
  ts_utc: string;
  last_close: number;
  expected_return: number;
  expected_price: number;
  p_up: number | null;
  interval_low: number;
  interval_high: number;
  model_version: string;
  model_timestamp_utc: string;
}

export interface RiskLatest {
  symbol: string;
  horizon: string;
  timeframe: string;
  ts_utc: string;
  expected_return: number;
  interval_low: number;
  interval_high: number;
  p_return_below_minus_1pct: number;
  p_return_below_minus_2pct: number;
}

export interface Bar {
  symbol: string;
  timeframe: string;
  ts_utc: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number | null;
}

export interface BarsResponse {
  symbol: string;
  timeframe: string;
  bars: Bar[];
}

export interface SymbolListResponse {
  symbols: string[];
}

export interface HealthResponse {
  ok: boolean;
  time_utc: string;
}

export interface AIInsight {
  id: string;
  category: 'OPPORTUNITY' | 'RISK DETECTED' | 'TREND' | 'RECOMMENDATION';
  title: string;
  description: string;
  impact: 'POSITIVE' | 'NEUTRAL' | 'WARNING' | 'CRITICAL';
  metric?: string;
  value?: string;
}

export interface WatchlistItem {
  symbol: string;
  last_close?: number;
  expected_return?: number;
  p_up?: number | null;
  advice?: string;
}

export interface User {
  id: number;
  username: string;
}

export interface AuthResponse {
  ok: boolean;
  user: User;
  token: string;
}

export interface UserStrategy {
  name: string;
  min_return: number;
  min_p_up: number;
  max_downside: number;
  notes?: string;
}

export interface AIChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  timestamp: string;
  context?: {
    symbol?: string;
    horizon?: string;
    expected_return?: number;
    p_up?: number | null;
    advice?: string;
  };
}
