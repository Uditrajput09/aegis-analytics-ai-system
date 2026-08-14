import React, { useState, useEffect } from 'react';
import {
  DollarSign,
  Percent,
  ShieldAlert,
  Sparkles,
  RefreshCw,
  ArrowUpRight,
  ArrowDownRight,
  Cpu,
} from 'lucide-react';
import {
  ResponsiveContainer,
  ComposedChart,
  Area,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';
import { apiService } from '../services/api';
import type { PredictionLatest, RiskLatest, Bar as PriceBar, AIInsight } from '../types/api';

interface OverviewPageProps {
  symbol: string;
  onSymbolChange: (symbol: string) => void;
  availableSymbols: string[];
}

export const OverviewPage: React.FC<OverviewPageProps> = ({
  symbol,
  onSymbolChange,
  availableSymbols,
}) => {
  const [horizon, setHorizon] = useState<'5m' | '15m' | '60m' | '1d'>('5m');
  const [timeframe, setTimeframe] = useState<'1m' | '1d'>('1m');
  const [prediction, setPrediction] = useState<PredictionLatest | null>(null);
  const [risk, setRisk] = useState<RiskLatest | null>(null);
  const [bars, setBars] = useState<PriceBar[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const tf = horizon === '1d' ? '1d' : timeframe;
      const [predData, riskData, barsData] = await Promise.all([
        apiService.getLatestPrediction(symbol, horizon, tf),
        apiService.getLatestRisk(symbol, horizon, tf),
        apiService.getRecentBars(symbol, tf, 100),
      ]);
      setPrediction(predData);
      setRisk(riskData);
      setBars(barsData.bars || []);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch Aegis telemetry data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [symbol, horizon, timeframe]);

  // Derived signal & insights
  const signal = prediction && risk ? apiService.deriveSignal(prediction, risk) : null;
  const insights: AIInsight[] = prediction && risk ? apiService.deriveAIInsights(prediction, risk) : [];

  // Chart data formatting with moving average calculation
  const chartData = bars.map((b, idx, arr) => {
    // 20-period moving average calculation
    const window20 = arr.slice(Math.max(0, idx - 19), idx + 1);
    const ma20 = window20.reduce((acc, curr) => acc + curr.close, 0) / window20.length;

    const timeStr = new Date(b.ts_utc).toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    });

    return {
      time: timeStr,
      rawTs: b.ts_utc,
      open: b.open,
      high: b.high,
      low: b.low,
      close: b.close,
      volume: b.volume || 0,
      ma20: parseFloat(ma20.toFixed(2)),
      isUp: b.close >= b.open,
    };
  });

  return (
    <div className="space-y-6 pb-12">
      {/* HEADER SECTION */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-panel p-6 rounded-2xl">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
              Welcome back
            </h1>
            <span className="text-2xl">👋</span>
          </div>
          <p className="text-slate-400 text-sm mt-1">
            Here's what Aegis found in your market data.
          </p>
        </div>

        {/* SYMBOL & HORIZON SELECTORS */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2 bg-aegis-bg-subtle border border-aegis-border px-3.5 py-2 rounded-xl">
            <span className="text-xs text-slate-400 font-semibold uppercase">Symbol</span>
            <select
              value={symbol}
              onChange={e => onSymbolChange(e.target.value)}
              className="bg-transparent text-sm font-bold text-white focus:outline-none cursor-pointer"
            >
              {availableSymbols.map(s => (
                <option key={s} value={s} className="bg-aegis-card text-white">
                  {s}
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center bg-aegis-bg-subtle border border-aegis-border p-1 rounded-xl">
            {(['5m', '15m', '60m', '1d'] as const).map(h => (
              <button
                key={h}
                onClick={() => setHorizon(h)}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                  horizon === h
                    ? 'bg-purple-gradient text-white shadow-glow-sm'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {h}
              </button>
            ))}
          </div>

          <button
            onClick={loadData}
            disabled={loading}
            className="p-2.5 rounded-xl bg-aegis-card border border-aegis-border hover:border-aegis-primary-bright text-slate-300 hover:text-white transition-all disabled:opacity-50"
            title="Refresh market data"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* ERROR ALERT */}
      {error && (
        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-aegis-risk flex items-center justify-between text-sm">
          <span>{error}</span>
          <button onClick={loadData} className="underline text-xs font-bold">
            Retry
          </button>
        </div>
      )}

      {/* 4 KPI CARDS */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* CARD 1: CURRENT PRICE */}
        <div className="glass-panel-interactive p-5 rounded-2xl flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Current Price
            </span>
            <div className="p-2 rounded-xl bg-purple-500/10 text-aegis-primary-bright border border-purple-500/20">
              <DollarSign className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <h3 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
              {loading ? (
                <span className="animate-pulse text-slate-600">₹----.--</span>
              ) : (
                `₹${prediction?.last_close?.toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2,
                })}`
              )}
            </h3>
            <p className="text-xs text-slate-400 mt-1 flex items-center gap-1">
              <span>Timeframe:</span>
              <span className="text-slate-200 font-semibold">{prediction?.timeframe || horizon}</span>
            </p>
          </div>
        </div>

        {/* CARD 2: EXPECTED RETURN */}
        <div className="glass-panel-interactive p-5 rounded-2xl flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Expected Return
            </span>
            <div className="p-2 rounded-xl bg-indigo-500/10 text-aegis-secondary border border-indigo-500/20">
              <Percent className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <h3
              className={`text-2xl md:text-3xl font-extrabold tracking-tight flex items-center gap-1 ${
                (prediction?.expected_return || 0) >= 0
                  ? 'text-aegis-positive'
                  : 'text-aegis-risk'
              }`}
            >
              {loading ? (
                <span className="animate-pulse text-slate-600">+--.--%</span>
              ) : (
                <>
                  {(prediction?.expected_return || 0) >= 0 ? (
                    <ArrowUpRight className="w-6 h-6" />
                  ) : (
                    <ArrowDownRight className="w-6 h-6" />
                  )}
                  {`${((prediction?.expected_return || 0) * 100).toFixed(2)}%`}
                </>
              )}
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Target Price:{' '}
              <span className="text-white font-semibold">
                ₹{prediction?.expected_price?.toFixed(2)}
              </span>
            </p>
          </div>
        </div>

        {/* CARD 3: PROBABILITY UP */}
        <div className="glass-panel-interactive p-5 rounded-2xl flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Probability Up
            </span>
            <div className="p-2 rounded-xl bg-purple-500/10 text-aegis-ai border border-purple-500/20">
              <Sparkles className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <h3 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
              {loading ? (
                <span className="animate-pulse text-slate-600">--.-%</span>
              ) : prediction?.p_up !== null && prediction?.p_up !== undefined ? (
                `${(prediction.p_up * 100).toFixed(1)}%`
              ) : (
                <span className="text-slate-500 text-lg">N/A</span>
              )}
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Isotonic Calibrated Confidence
            </p>
          </div>
        </div>

        {/* CARD 4: RISK */}
        <div className="glass-panel-interactive p-5 rounded-2xl flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Downside Risk (-2%)
            </span>
            <div className="p-2 rounded-xl bg-red-500/10 text-aegis-risk border border-red-500/20">
              <ShieldAlert className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <h3
              className={`text-2xl md:text-3xl font-extrabold tracking-tight ${
                (risk?.p_return_below_minus_2pct || 0) > 0.2
                  ? 'text-aegis-risk'
                  : 'text-emerald-400'
              }`}
            >
              {loading ? (
                <span className="animate-pulse text-slate-600">--.-%</span>
              ) : (
                `${((risk?.p_return_below_minus_2pct || 0) * 100).toFixed(1)}%`
              )}
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              P(Return &lt; -1%):{' '}
              <span className="text-slate-200 font-semibold">
                {((risk?.p_return_below_minus_1pct || 0) * 100).toFixed(1)}%
              </span>
            </p>
          </div>
        </div>
      </div>

      {/* MAIN DASHBOARD CONTENT GRID */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* MARKET PERFORMANCE CHART (COL SPAN 2) */}
        <div className="lg:col-span-2 glass-panel p-6 rounded-2xl flex flex-col space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h2 className="text-lg font-bold text-white tracking-wide">Market Performance</h2>
              <p className="text-xs text-slate-400">
                Price action and technical indicators for {symbol}
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-400">Timeframe:</span>
              <button
                onClick={() => setTimeframe('1m')}
                disabled={horizon === '1d'}
                className={`px-2.5 py-1 rounded-lg text-xs font-semibold ${
                  timeframe === '1m' && horizon !== '1d'
                    ? 'bg-aegis-primary text-white'
                    : 'text-slate-400 bg-aegis-bg-subtle'
                }`}
              >
                1m
              </button>
              <button
                onClick={() => setTimeframe('1d')}
                className={`px-2.5 py-1 rounded-lg text-xs font-semibold ${
                  timeframe === '1d' || horizon === '1d'
                    ? 'bg-aegis-primary text-white'
                    : 'text-slate-400 bg-aegis-bg-subtle'
                }`}
              >
                1d
              </button>
            </div>
          </div>

          {/* CHART CANVAS */}
          <div className="h-80 w-full pt-4">
            {loading ? (
              <div className="h-full w-full flex items-center justify-center text-slate-500 animate-pulse">
                Loading Market Data...
              </div>
            ) : chartData.length === 0 ? (
              <div className="h-full w-full flex items-center justify-center text-slate-500">
                No recent price bars available
              </div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={chartData}>
                  <defs>
                    <linearGradient id="priceGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#8B5CF6" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#8B5CF6" stopOpacity={0.0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(139, 92, 246, 0.1)" />
                  <XAxis dataKey="time" stroke="#64748B" tick={{ fontSize: 11 }} />
                  <YAxis
                    domain={['auto', 'auto']}
                    stroke="#64748B"
                    tick={{ fontSize: 11 }}
                    orientation="right"
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#141226',
                      borderColor: 'rgba(139, 92, 246, 0.3)',
                      borderRadius: '12px',
                      color: '#fff',
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="close"
                    stroke="#8B5CF6"
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#priceGradient)"
                    name="Close Price"
                  />
                  <Line
                    type="monotone"
                    dataKey="ma20"
                    stroke="#6366F1"
                    strokeWidth={1.5}
                    dot={false}
                    name="MA 20"
                  />
                </ComposedChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        {/* AEGIS PREDICTION PANEL & CONFIDENCE (COL SPAN 1) */}
        <div className="space-y-6">
          {/* PREDICTION CARD */}
          <div className="glass-panel p-6 rounded-2xl space-y-5">
            <div className="flex items-center justify-between border-b border-aegis-border/50 pb-4">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-aegis-primary/20 flex items-center justify-center text-aegis-primary-bright">
                  <Cpu className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="font-bold text-white text-base">Aegis Prediction</h3>
                  <p className="text-[10px] text-slate-400">Horizon: {horizon}</p>
                </div>
              </div>
              {signal && (
                <span className={`px-3 py-1 rounded-full text-xs font-bold border ${signal.color}`}>
                  {signal.label}
                </span>
              )}
            </div>

            {/* PREDICTION METRIC BREAKDOWN */}
            <div className="space-y-3">
              <div className="flex justify-between items-center py-1 border-b border-white/5">
                <span className="text-xs text-slate-400">Expected Price</span>
                <span className="text-sm font-bold text-white">
                  ₹{prediction?.expected_price?.toFixed(2)}
                </span>
              </div>
              <div className="flex justify-between items-center py-1 border-b border-white/5">
                <span className="text-xs text-slate-400">Target Horizon</span>
                <span className="text-sm font-bold text-aegis-primary-bright">{horizon}</span>
              </div>
              <div className="flex justify-between items-center py-1 border-b border-white/5">
                <span className="text-xs text-slate-400">90% Prediction Band</span>
                <span className="text-xs font-bold text-slate-200">
                  {prediction
                    ? `${(prediction.interval_low * 100).toFixed(2)}% to +${(
                        prediction.interval_high * 100
                      ).toFixed(2)}%`
                    : '---'}
                </span>
              </div>
              <div className="flex justify-between items-center py-1 border-b border-white/5">
                <span className="text-xs text-slate-400">Model Version</span>
                <span className="text-xs font-semibold text-slate-400">
                  {prediction?.model_version || 'mvp_v1'}
                </span>
              </div>
            </div>

            {/* PREDICTION CONFIDENCE GAUGE VISUALIZATION */}
            <div className="pt-2">
              <div className="flex justify-between items-center mb-1.5">
                <span className="text-xs font-semibold text-slate-300">Prediction Confidence</span>
                <span className="text-xs font-bold text-aegis-ai">
                  {prediction?.p_up ? `${(prediction.p_up * 100).toFixed(1)}%` : '50%'}
                </span>
              </div>
              <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden p-0.5 border border-aegis-border/50">
                <div
                  className="bg-gradient-to-r from-indigo-500 via-purple-500 to-aegis-ai h-full rounded-full transition-all duration-500"
                  style={{ width: `${(prediction?.p_up || 0.5) * 100}%` }}
                />
              </div>
              <p className="text-[10px] text-slate-400 mt-1.5 text-center">
                Isotonic direction score mapped from LightGBM dual-head classifier.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* AEGIS AI INSIGHTS SECTION */}
      <div className="space-y-4">
        <div>
          <h2 className="text-xl font-extrabold text-white tracking-wide flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-aegis-ai" />
            AEGIS AI INSIGHTS
          </h2>
          <p className="text-xs text-slate-400">Understand what the latest market data means.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {insights.map(item => (
            <div key={item.id} className="glass-panel-interactive p-5 rounded-2xl flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span
                    className={`text-[10px] font-bold px-2.5 py-1 rounded-full uppercase tracking-wider ${
                      item.category === 'OPPORTUNITY'
                        ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                        : item.category === 'RISK DETECTED'
                        ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                        : item.category === 'TREND'
                        ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30'
                        : 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                    }`}
                  >
                    {item.category}
                  </span>
                  {item.value && (
                    <span className="text-xs font-extrabold text-white bg-aegis-card px-2 py-0.5 rounded-md border border-aegis-border">
                      {item.value}
                    </span>
                  )}
                </div>
                <h4 className="font-bold text-white text-sm leading-snug">{item.title}</h4>
                <p className="text-xs text-slate-400 mt-2 leading-relaxed">{item.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
