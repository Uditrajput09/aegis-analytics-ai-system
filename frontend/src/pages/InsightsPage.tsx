import React, { useState, useEffect } from 'react';
import { Sparkles, RefreshCw } from 'lucide-react';
import { apiService } from '../services/api';
import type { PredictionLatest, RiskLatest, AIInsight } from '../types/api';

interface InsightsPageProps {
  symbol: string;
}

export const InsightsPage: React.FC<InsightsPageProps> = ({ symbol }) => {
  const [prediction, setPrediction] = useState<PredictionLatest | null>(null);
  const [risk, setRisk] = useState<RiskLatest | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [filter, setFilter] = useState<string>('ALL');

  const loadData = async () => {
    setLoading(true);
    try {
      const [p, r] = await Promise.all([
        apiService.getLatestPrediction(symbol, '5m', '1m'),
        apiService.getLatestRisk(symbol, '5m', '1m'),
      ]);
      setPrediction(p);
      setRisk(r);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [symbol]);

  const rawInsights: AIInsight[] = prediction && risk ? apiService.deriveAIInsights(prediction, risk) : [];
  const filteredInsights = filter === 'ALL' ? rawInsights : rawInsights.filter(i => i.category === filter);

  return (
    <div className="space-y-6 pb-12">
      {/* HEADER */}
      <div className="glass-panel p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-aegis-ai" />
            AEGIS AI INSIGHTS
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Quantitative interpretation and intelligent market narrative for{' '}
            <span className="text-aegis-primary-bright font-bold">{symbol}</span>.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center bg-aegis-bg-subtle border border-aegis-border p-1 rounded-xl">
            {['ALL', 'OPPORTUNITY', 'RISK DETECTED', 'TREND', 'RECOMMENDATION'].map(cat => (
              <button
                key={cat}
                onClick={() => setFilter(cat)}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                  filter === cat
                    ? 'bg-purple-gradient text-white shadow-glow-sm'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
          <button
            onClick={loadData}
            className="p-2.5 rounded-xl glass-panel text-slate-300 hover:text-white"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* INSIGHTS CARDS GRID */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 animate-pulse">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="h-44 glass-panel rounded-2xl" />
          ))}
        </div>
      ) : filteredInsights.length === 0 ? (
        <div className="glass-panel p-12 text-center text-slate-400 rounded-2xl">
          No insights matching category "{filter}".
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {filteredInsights.map(item => (
            <div key={item.id} className="glass-panel-interactive p-6 rounded-2xl space-y-4">
              <div className="flex items-center justify-between">
                <span
                  className={`text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider ${
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
                  <span className="text-sm font-extrabold text-aegis-primary-bright bg-aegis-bg-subtle px-3 py-1 rounded-xl border border-aegis-border">
                    {item.value}
                  </span>
                )}
              </div>

              <div>
                <h3 className="font-bold text-lg text-white">{item.title}</h3>
                <p className="text-sm text-slate-300 mt-2 leading-relaxed">{item.description}</p>
              </div>

              {item.metric && (
                <div className="pt-3 border-t border-aegis-border/40 flex items-center justify-between text-xs">
                  <span className="text-slate-400">Target Metric</span>
                  <span className="font-semibold text-slate-200">{item.metric}</span>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
