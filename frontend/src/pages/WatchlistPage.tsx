import React, { useState, useEffect } from 'react';
import { Bookmark, Plus, Trash2 } from 'lucide-react';
import { apiService } from '../services/api';
import type { PredictionLatest, RiskLatest } from '../types/api';

interface WatchlistPageProps {
  onSelectSymbol: (symbol: string) => void;
}

interface WatchlistItemData {
  symbol: string;
  prediction?: PredictionLatest;
  risk?: RiskLatest;
  loading: boolean;
}

export const WatchlistPage: React.FC<WatchlistPageProps> = ({ onSelectSymbol }) => {
  const [watchlist, setWatchlist] = useState<string[]>(['RELIANCE.NS', 'TCS.NS', 'AAPL']);
  const [itemsData, setItemsData] = useState<Record<string, WatchlistItemData>>({});
  const [newSymbolInput, setNewSymbolInput] = useState('');

  const loadWatchlistData = async () => {
    const newItems: Record<string, WatchlistItemData> = {};
    for (const sym of watchlist) {
      newItems[sym] = { symbol: sym, loading: true };
    }
    setItemsData(newItems);

    for (const sym of watchlist) {
      try {
        const [p, r] = await Promise.all([
          apiService.getLatestPrediction(sym, '5m', '1m'),
          apiService.getLatestRisk(sym, '5m', '1m'),
        ]);
        setItemsData(prev => ({
          ...prev,
          [sym]: { symbol: sym, prediction: p, risk: r, loading: false },
        }));
      } catch (err) {
        setItemsData(prev => ({
          ...prev,
          [sym]: { symbol: sym, loading: false },
        }));
      }
    }
  };

  useEffect(() => {
    loadWatchlistData();
  }, [watchlist]);

  const handleAdd = () => {
    const s = newSymbolInput.trim().toUpperCase();
    if (s && !watchlist.includes(s)) {
      setWatchlist([...watchlist, s]);
      setNewSymbolInput('');
    }
  };

  const handleRemove = (sym: string) => {
    setWatchlist(watchlist.filter(item => item !== sym));
  };

  return (
    <div className="space-y-6 pb-12">
      {/* HEADER */}
      <div className="glass-panel p-6 rounded-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <Bookmark className="w-6 h-6 text-aegis-primary-bright" />
            Watchlist
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Track key equity assets with live LightGBM return expectations and downside risk.
          </p>
        </div>

        {/* ADD SYMBOL INPUT */}
        <div className="flex items-center gap-2">
          <div className="relative">
            <input
              type="text"
              placeholder="Add Ticker Symbol..."
              value={newSymbolInput}
              onChange={e => setNewSymbolInput(e.target.value)}
              className="bg-aegis-bg-subtle border border-aegis-border rounded-xl px-3 py-2 text-xs text-white placeholder-slate-400 focus:outline-none focus:border-aegis-primary-bright"
            />
          </div>
          <button
            onClick={handleAdd}
            className="px-3 py-2 rounded-xl bg-purple-gradient text-xs font-bold text-white shadow-glow-sm flex items-center gap-1"
          >
            <Plus className="w-4 h-4" />
            <span>Add</span>
          </button>
        </div>
      </div>

      {/* WATCHLIST CARDS TABLE */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-aegis-bg-subtle text-slate-400 font-semibold border-b border-aegis-border/50">
              <tr>
                <th className="p-3">Symbol</th>
                <th className="p-3">Last Close</th>
                <th className="p-3">Expected Return</th>
                <th className="p-3">Probability Up</th>
                <th className="p-3">Downside Risk (-2%)</th>
                <th className="p-3">Signal</th>
                <th className="p-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-aegis-border/30">
              {watchlist.map(sym => {
                const data = itemsData[sym];
                const pred = data?.prediction;
                const risk = data?.risk;
                const signal = pred && risk ? apiService.deriveSignal(pred, risk) : null;

                return (
                  <tr key={sym} className="hover:bg-white/5 text-slate-200">
                    <td className="p-3 font-extrabold text-white">{sym}</td>
                    <td className="p-3 font-semibold">
                      {data?.loading ? (
                        <span className="animate-pulse text-slate-600">₹---.--</span>
                      ) : pred ? (
                        `₹${pred.last_close.toFixed(2)}`
                      ) : (
                        'N/A'
                      )}
                    </td>
                    <td
                      className={`p-3 font-bold ${
                        (pred?.expected_return || 0) >= 0 ? 'text-aegis-positive' : 'text-aegis-risk'
                      }`}
                    >
                      {data?.loading ? (
                        <span className="animate-pulse text-slate-600">--.--%</span>
                      ) : pred ? (
                        `${(pred.expected_return * 100).toFixed(2)}%`
                      ) : (
                        'N/A'
                      )}
                    </td>
                    <td className="p-3 font-semibold text-aegis-ai">
                      {pred?.p_up ? `${(pred.p_up * 100).toFixed(1)}%` : '---'}
                    </td>
                    <td className="p-3 font-semibold text-aegis-risk">
                      {risk ? `${(risk.p_return_below_minus_2pct * 100).toFixed(1)}%` : '---'}
                    </td>
                    <td className="p-3">
                      {signal ? (
                        <span className={`px-2.5 py-0.5 rounded-full font-bold border ${signal.color}`}>
                          {signal.label}
                        </span>
                      ) : (
                        '---'
                      )}
                    </td>
                    <td className="p-3 text-right space-x-2">
                      <button
                        onClick={() => onSelectSymbol(sym)}
                        className="px-2.5 py-1 rounded-lg bg-aegis-primary/20 text-aegis-primary-bright hover:bg-aegis-primary/40 font-semibold"
                      >
                        Analyze
                      </button>
                      <button
                        onClick={() => handleRemove(sym)}
                        className="p-1 rounded-lg text-slate-400 hover:text-red-400 hover:bg-red-500/10"
                        title="Remove from watchlist"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
