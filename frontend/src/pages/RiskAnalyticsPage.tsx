import React, { useState, useEffect } from 'react';
import { ShieldAlert, AlertTriangle, RefreshCw, Lock } from 'lucide-react';
import { apiService } from '../services/api';
import type { RiskLatest, PredictionLatest } from '../types/api';

interface RiskAnalyticsPageProps {
  symbol: string;
}

export const RiskAnalyticsPage: React.FC<RiskAnalyticsPageProps> = ({ symbol }) => {
  const [horizon, setHorizon] = useState<'5m' | '15m' | '60m' | '1d'>('5m');
  const [risk, setRisk] = useState<RiskLatest | null>(null);
  const [prediction, setPrediction] = useState<PredictionLatest | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const loadRisk = async () => {
    setLoading(true);
    try {
      const tf = horizon === '1d' ? '1d' : '1m';
      const [rData, pData] = await Promise.all([
        apiService.getLatestRisk(symbol, horizon, tf),
        apiService.getLatestPrediction(symbol, horizon, tf),
      ]);
      setRisk(rData);
      setPrediction(pData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRisk();
  }, [symbol, horizon]);

  const pDown1 = (risk?.p_return_below_minus_1pct || 0) * 100;
  const pDown2 = (risk?.p_return_below_minus_2pct || 0) * 100;
  const lowPct = (prediction?.interval_low || 0) * 100;
  const highPct = (prediction?.interval_high || 0) * 100;
  const widthPct = Math.abs(highPct - lowPct);

  return (
    <div className="space-y-6 pb-12">
      {/* HEADER */}
      <div className="glass-panel p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <ShieldAlert className="w-6 h-6 text-aegis-risk" />
            Statistical Risk Analytics
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Conformal empirical tail-risk and downside loss probability estimation for{' '}
            <span className="text-aegis-primary-bright font-bold">{symbol}</span>.
          </p>
        </div>

        <div className="flex items-center gap-3">
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
            onClick={loadRisk}
            className="p-2.5 rounded-xl glass-panel text-slate-300 hover:text-white"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* TAIL LOSS RISK CARDS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* CARD 1: P(RETURN < -1%) */}
        <div className="glass-panel-interactive p-6 rounded-2xl flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              P(Return &lt; -1.0%)
            </span>
            <AlertTriangle className="w-5 h-5 text-amber-400" />
          </div>
          <div className="mt-4">
            <h2 className="text-3xl font-extrabold text-white">
              {loading ? <span className="animate-pulse text-slate-600">--.-%</span> : `${pDown1.toFixed(2)}%`}
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Probability of mild drawdown (&gt;1% loss)
            </p>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full mt-4 overflow-hidden">
            <div
              className="bg-amber-400 h-full rounded-full transition-all duration-500"
              style={{ width: `${Math.min(100, pDown1)}%` }}
            />
          </div>
        </div>

        {/* CARD 2: P(RETURN < -2%) */}
        <div className="glass-panel-interactive p-6 rounded-2xl flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              P(Return &lt; -2.0%)
            </span>
            <ShieldAlert className="w-5 h-5 text-aegis-risk" />
          </div>
          <div className="mt-4">
            <h2 className="text-3xl font-extrabold text-aegis-risk">
              {loading ? <span className="animate-pulse text-slate-600">--.-%</span> : `${pDown2.toFixed(2)}%`}
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Probability of severe downside tail event
            </p>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full mt-4 overflow-hidden">
            <div
              className="bg-aegis-risk h-full rounded-full transition-all duration-500"
              style={{ width: `${Math.min(100, pDown2)}%` }}
            />
          </div>
        </div>

        {/* CARD 3: CONFORMAL BAND WIDTH */}
        <div className="glass-panel-interactive p-6 rounded-2xl flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              90% Interval Spread
            </span>
            <Lock className="w-5 h-5 text-aegis-primary-bright" />
          </div>
          <div className="mt-4">
            <h2 className="text-3xl font-extrabold text-white">
              {loading ? <span className="animate-pulse text-slate-600">--.--%</span> : `${widthPct.toFixed(2)}%`}
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Conformal distribution width ($\alpha=0.10$)
            </p>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full mt-4 overflow-hidden">
            <div
              className="bg-aegis-primary-bright h-full rounded-full transition-all duration-500"
              style={{ width: `${Math.min(100, widthPct * 20)}%` }}
            />
          </div>
        </div>
      </div>

      {/* CONFORMAL PREDICTION INTERVAL VISUALIZATION */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <h3 className="font-bold text-white text-base">Conformal Prediction Range Bounds</h3>
        <p className="text-xs text-slate-400">
          Statistically distribution-free bounds guaranteeing 90% finite-sample coverage over the{' '}
          <span className="text-white font-semibold">{horizon}</span> horizon.
        </p>

        <div className="p-6 rounded-xl bg-aegis-bg-subtle border border-aegis-border space-y-4">
          <div className="flex justify-between text-xs font-bold">
            <span className="text-aegis-risk">Lower Bound: {lowPct.toFixed(2)}%</span>
            <span className="text-white">Point Prediction: {((prediction?.expected_return || 0) * 100).toFixed(2)}%</span>
            <span className="text-aegis-positive">Upper Bound: +{highPct.toFixed(2)}%</span>
          </div>

          <div className="relative w-full h-8 bg-slate-800 rounded-xl flex items-center px-4 overflow-hidden">
            <div className="w-full h-2 bg-gradient-to-r from-red-500 via-indigo-500 to-emerald-500 rounded-full" />
          </div>

          <div className="grid grid-cols-2 gap-4 pt-2 text-xs">
            <div className="p-3 rounded-lg bg-aegis-card border border-aegis-border">
              <span className="text-slate-400">Lower Bound Target Price:</span>
              <p className="text-base font-bold text-red-400 mt-0.5">
                ₹{((prediction?.last_close || 0) * (1 + (prediction?.interval_low || 0))).toFixed(2)}
              </p>
            </div>
            <div className="p-3 rounded-lg bg-aegis-card border border-aegis-border">
              <span className="text-slate-400">Upper Bound Target Price:</span>
              <p className="text-base font-bold text-emerald-400 mt-0.5">
                ₹{((prediction?.last_close || 0) * (1 + (prediction?.interval_high || 0))).toFixed(2)}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
