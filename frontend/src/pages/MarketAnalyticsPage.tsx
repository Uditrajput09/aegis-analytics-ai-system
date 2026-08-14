import React, { useState, useEffect } from 'react';
import { TrendingUp, RefreshCw } from 'lucide-react';
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
import type { Bar as PriceBar } from '../types/api';

interface MarketAnalyticsPageProps {
  symbol: string;
}

export const MarketAnalyticsPage: React.FC<MarketAnalyticsPageProps> = ({ symbol }) => {
  const [timeframe, setTimeframe] = useState<'1m' | '1d'>('1m');
  const [limit, setLimit] = useState<number>(300);
  const [showMA20, setShowMA20] = useState<boolean>(true);
  const [showMA50, setShowMA50] = useState<boolean>(true);
  const [bars, setBars] = useState<PriceBar[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const loadData = async () => {
    setLoading(true);
    try {
      const res = await apiService.getRecentBars(symbol, timeframe, limit);
      setBars(res.bars || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [symbol, timeframe, limit]);

  const formattedChartData = bars.map((b, idx, arr) => {
    // MA 20
    const w20 = arr.slice(Math.max(0, idx - 19), idx + 1);
    const ma20 = w20.reduce((acc, c) => acc + c.close, 0) / w20.length;

    // MA 50
    const w50 = arr.slice(Math.max(0, idx - 49), idx + 1);
    const ma50 = w50.reduce((acc, c) => acc + c.close, 0) / w50.length;

    const timeStr = new Date(b.ts_utc).toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    });

    return {
      time: timeStr,
      open: b.open,
      high: b.high,
      low: b.low,
      close: b.close,
      volume: b.volume || 0,
      ma20: parseFloat(ma20.toFixed(2)),
      ma50: parseFloat(ma50.toFixed(2)),
    };
  });

  return (
    <div className="space-y-6 pb-12">
      {/* HEADER & CONTROLS */}
      <div className="glass-panel p-6 rounded-2xl flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <TrendingUp className="w-6 h-6 text-aegis-primary-bright" />
            Market Analytics
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Technical price movement and moving average overlays for{' '}
            <span className="text-aegis-primary-bright font-bold">{symbol}</span>.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* TIMEFRAME */}
          <div className="flex items-center bg-aegis-bg-subtle border border-aegis-border p-1 rounded-xl">
            {(['1m', '1d'] as const).map(tf => (
              <button
                key={tf}
                onClick={() => setTimeframe(tf)}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                  timeframe === tf
                    ? 'bg-purple-gradient text-white shadow-glow-sm'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {tf}
              </button>
            ))}
          </div>

          {/* LIMIT */}
          <div className="flex items-center gap-2 bg-aegis-bg-subtle border border-aegis-border px-3 py-1.5 rounded-xl">
            <span className="text-xs text-slate-400 font-semibold">Bars:</span>
            <select
              value={limit}
              onChange={e => setLimit(Number(e.target.value))}
              className="bg-transparent text-xs font-bold text-white focus:outline-none cursor-pointer"
            >
              <option value={100} className="bg-aegis-card">
                100
              </option>
              <option value={300} className="bg-aegis-card">
                300
              </option>
              <option value={500} className="bg-aegis-card">
                500
              </option>
            </select>
          </div>

          {/* MA TOGGLES */}
          <button
            onClick={() => setShowMA20(!showMA20)}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold border transition-all ${
              showMA20
                ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500/40'
                : 'text-slate-500 border-aegis-border bg-aegis-bg-subtle'
            }`}
          >
            MA 20
          </button>
          <button
            onClick={() => setShowMA50(!showMA50)}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold border transition-all ${
              showMA50
                ? 'bg-purple-500/20 text-purple-300 border-purple-500/40'
                : 'text-slate-500 border-aegis-border bg-aegis-bg-subtle'
            }`}
          >
            MA 50
          </button>

          <button
            onClick={loadData}
            className="p-2.5 rounded-xl glass-panel text-slate-300 hover:text-white"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* CHART PANEL */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <div className="h-96 w-full">
          {loading ? (
            <div className="h-full flex items-center justify-center text-slate-500 animate-pulse">
              Loading Chart Data...
            </div>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={formattedChartData}>
                <defs>
                  <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#7C3AED" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#7C3AED" stopOpacity={0.0} />
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
                  fill="url(#areaGradient)"
                  name="Close Price"
                />
                {showMA20 && (
                  <Line
                    type="monotone"
                    dataKey="ma20"
                    stroke="#6366F1"
                    strokeWidth={1.5}
                    dot={false}
                    name="MA 20"
                  />
                )}
                {showMA50 && (
                  <Line
                    type="monotone"
                    dataKey="ma50"
                    stroke="#A855F7"
                    strokeWidth={1.5}
                    dot={false}
                    name="MA 50"
                  />
                )}
              </ComposedChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      {/* OHLCV RECENT TABLE */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <h3 className="font-bold text-white text-base">Recent OHLCV Data Bars</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-aegis-bg-subtle text-slate-400 font-semibold border-b border-aegis-border/50">
              <tr>
                <th className="p-3">Time (UTC)</th>
                <th className="p-3">Open</th>
                <th className="p-3">High</th>
                <th className="p-3">Low</th>
                <th className="p-3">Close</th>
                <th className="p-3">Volume</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-aegis-border/30">
              {bars.slice(-15).reverse().map((b, i) => (
                <tr key={i} className="hover:bg-white/5 text-slate-200">
                  <td className="p-3 font-mono text-slate-400">
                    {new Date(b.ts_utc).toLocaleString()}
                  </td>
                  <td className="p-3 font-semibold">₹{b.open.toFixed(2)}</td>
                  <td className="p-3 font-semibold text-emerald-400">₹{b.high.toFixed(2)}</td>
                  <td className="p-3 font-semibold text-red-400">₹{b.low.toFixed(2)}</td>
                  <td className="p-3 font-bold text-white">₹{b.close.toFixed(2)}</td>
                  <td className="p-3 text-slate-400">{b.volume?.toLocaleString() || '---'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
