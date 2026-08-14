import React, { useState, useEffect } from 'react';
import { LineChart, RefreshCw, Trophy } from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell,
} from 'recharts';
import { apiService } from '../services/api';
import type { PredictionLatest } from '../types/api';

interface ForecastsPageProps {
  symbol: string;
}

export const ForecastsPage: React.FC<ForecastsPageProps> = ({ symbol }) => {
  const [predictions, setPredictions] = useState<Record<string, PredictionLatest>>({});
  const [loading, setLoading] = useState<boolean>(true);

  const loadMultiHorizon = async () => {
    setLoading(true);
    try {
      const data = await apiService.getMultiHorizonPredictions(symbol);
      setPredictions(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMultiHorizon();
  }, [symbol]);

  const horizons = ['5m', '15m', '60m', '1d'] as const;

  // Best horizon calculation
  const validPredictions = Object.values(predictions);
  const bestPrediction = validPredictions.length
    ? validPredictions.reduce((best, curr) =>
        curr.expected_return > best.expected_return ? curr : best
      )
    : null;

  const chartData = horizons.map(h => {
    const p = predictions[h];
    return {
      horizon: h,
      expected_return: p ? parseFloat((p.expected_return * 100).toFixed(2)) : 0,
      p_up: p?.p_up ? parseFloat((p.p_up * 100).toFixed(1)) : 50,
      isBest: bestPrediction?.horizon === h,
    };
  });

  return (
    <div className="space-y-6 pb-12">
      {/* HEADER */}
      <div className="glass-panel p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <LineChart className="w-6 h-6 text-aegis-primary-bright" />
            Multi-Horizon Forecast
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Compare LightGBM return predictions across 5m, 15m, 60m, and 1d horizons for{' '}
            <span className="text-aegis-primary-bright font-bold">{symbol}</span>.
          </p>
        </div>

        <button
          onClick={loadMultiHorizon}
          disabled={loading}
          className="p-2.5 rounded-xl glass-panel text-slate-300 hover:text-white flex items-center gap-2 text-sm font-semibold"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh Horizons</span>
        </button>
      </div>

      {/* STRONGEST HORIZON HIGHLIGHT BANNER */}
      {bestPrediction && (
        <div className="p-5 rounded-2xl bg-gradient-to-r from-purple-900/40 via-indigo-900/40 to-aegis-card border border-aegis-primary/40 flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-purple-gradient flex items-center justify-center text-white shadow-glow-purple flex-shrink-0">
            <Trophy className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-extrabold uppercase tracking-widest text-aegis-primary-bright">
                Strongest Forecast Horizon
              </span>
              <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-aegis-primary/30 text-white">
                {bestPrediction.horizon}
              </span>
            </div>
            <p className="text-sm font-bold text-white mt-0.5">
              Target return of +{(bestPrediction.expected_return * 100).toFixed(2)}% (Target Price: ₹
              {bestPrediction.expected_price.toFixed(2)})
            </p>
          </div>
        </div>
      )}

      {/* HORIZON SUMMARY CARDS GRID */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {horizons.map(h => {
          const p = predictions[h];
          const isBest = bestPrediction?.horizon === h;
          return (
            <div
              key={h}
              className={`glass-panel-interactive p-5 rounded-2xl flex flex-col justify-between relative overflow-hidden ${
                isBest ? 'border-aegis-primary-bright shadow-glow-sm' : ''
              }`}
            >
              {isBest && (
                <div className="absolute top-0 right-0 bg-aegis-primary text-[10px] font-bold px-2.5 py-1 rounded-bl-xl text-white">
                  TOP RANKED
                </div>
              )}
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Horizon: {h}
                </span>
                <h3 className="text-2xl font-extrabold text-white mt-2">
                  {loading || !p ? (
                    <span className="animate-pulse text-slate-600">--.--%</span>
                  ) : (
                    <span
                      className={
                        p.expected_return >= 0 ? 'text-aegis-positive' : 'text-aegis-risk'
                      }
                    >
                      {p.expected_return >= 0 ? '+' : ''}
                      {(p.expected_return * 100).toFixed(2)}%
                    </span>
                  )}
                </h3>
              </div>

              <div className="mt-4 pt-3 border-t border-aegis-border/40 space-y-1.5 text-xs">
                <div className="flex justify-between">
                  <span className="text-slate-400">Target Price:</span>
                  <span className="font-semibold text-white">
                    {p ? `₹${p.expected_price.toFixed(2)}` : '---'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">P(Up):</span>
                  <span className="font-semibold text-aegis-ai">
                    {p?.p_up ? `${(p.p_up * 100).toFixed(1)}%` : '---'}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* VISUAL COMPARISON CHART & MATRIX TABLE GRID */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* BAR CHART (COL SPAN 1) */}
        <div className="glass-panel p-6 rounded-2xl space-y-4">
          <h3 className="font-bold text-white text-base">Horizon Return Comparison</h3>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(139, 92, 246, 0.1)" />
                <XAxis dataKey="horizon" stroke="#64748B" />
                <YAxis stroke="#64748B" unit="%" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#141226',
                    borderColor: 'rgba(139, 92, 246, 0.3)',
                    borderRadius: '12px',
                    color: '#fff',
                  }}
                />
                <Bar dataKey="expected_return" name="Expected Return (%)" radius={[6, 6, 0, 0]}>
                  {chartData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={entry.expected_return >= 0 ? '#10B981' : '#EF4444'}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* COMPARISON MATRIX TABLE (COL SPAN 2) */}
        <div className="lg:col-span-2 glass-panel p-6 rounded-2xl space-y-4">
          <h3 className="font-bold text-white text-base">Multi-Horizon Comparison Matrix</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-aegis-bg-subtle text-slate-400 font-semibold border-b border-aegis-border/50">
                <tr>
                  <th className="p-3">Horizon</th>
                  <th className="p-3">Expected Return</th>
                  <th className="p-3">Expected Price</th>
                  <th className="p-3">P(Up)</th>
                  <th className="p-3">Conformal 90% Bounds</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-aegis-border/30">
                {horizons.map(h => {
                  const p = predictions[h];
                  const isBest = bestPrediction?.horizon === h;
                  return (
                    <tr
                      key={h}
                      className={`hover:bg-white/5 ${
                        isBest ? 'bg-purple-900/10 font-bold' : 'text-slate-200'
                      }`}
                    >
                      <td className="p-3">
                        <span className="px-2.5 py-1 rounded-lg bg-aegis-card font-mono border border-aegis-border">
                          {h}
                        </span>
                      </td>
                      <td
                        className={`p-3 font-bold ${
                          (p?.expected_return || 0) >= 0
                            ? 'text-aegis-positive'
                            : 'text-aegis-risk'
                        }`}
                      >
                        {p ? `${(p.expected_return * 100).toFixed(2)}%` : '---'}
                      </td>
                      <td className="p-3 font-semibold text-white">
                        {p ? `₹${p.expected_price.toFixed(2)}` : '---'}
                      </td>
                      <td className="p-3 font-semibold text-aegis-ai">
                        {p?.p_up ? `${(p.p_up * 100).toFixed(1)}%` : '---'}
                      </td>
                      <td className="p-3 font-mono text-slate-300">
                        {p
                          ? `${(p.interval_low * 100).toFixed(2)}% to +${(
                              p.interval_high * 100
                            ).toFixed(2)}%`
                          : '---'}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
