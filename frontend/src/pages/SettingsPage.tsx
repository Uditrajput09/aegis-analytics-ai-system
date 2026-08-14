import React, { useState, useEffect } from 'react';
import { Settings as SettingsIcon, Server, User, Sliders, RefreshCw } from 'lucide-react';
import { apiService } from '../services/api';

interface SettingsPageProps {
  symbol: string;
  onSymbolChange: (symbol: string) => void;
  availableSymbols: string[];
}

export const SettingsPage: React.FC<SettingsPageProps> = ({
  symbol,
  onSymbolChange,
  availableSymbols,
}) => {
  const [healthStatus, setHealthStatus] = useState<string>('Testing...');
  const [isOk, setIsOk] = useState<boolean | null>(null);
  const [testing, setTesting] = useState<boolean>(false);

  const testConnection = async () => {
    setTesting(true);
    try {
      const res = await apiService.getHealth();
      if (res.ok) {
        setHealthStatus(`Connected to Aegis REST API (${res.time_utc})`);
        setIsOk(true);
      }
    } catch (err: any) {
      setHealthStatus(err.message || 'Connection failed');
      setIsOk(false);
    } finally {
      setTesting(false);
    }
  };

  useEffect(() => {
    testConnection();
  }, []);

  return (
    <div className="space-y-6 pb-12 max-w-4xl">
      {/* HEADER */}
      <div className="glass-panel p-6 rounded-2xl">
        <h1 className="text-2xl font-extrabold text-white tracking-tight flex items-center gap-2">
          <SettingsIcon className="w-6 h-6 text-aegis-primary-bright" />
          Settings
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Configure API connection status, default ticker preferences, and system diagnostic state.
        </p>
      </div>

      {/* API CONNECTION STATUS PANEL */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <h3 className="font-bold text-white text-base flex items-center gap-2">
          <Server className="w-5 h-5 text-aegis-primary-bright" />
          Backend API Diagnostic Status
        </h3>

        <div className="p-4 rounded-xl bg-aegis-bg-subtle border border-aegis-border space-y-3">
          <div className="flex justify-between items-center text-xs">
            <span className="text-slate-400">FastAPI Base Endpoint</span>
            <span className="font-mono text-white bg-aegis-card px-2.5 py-1 rounded-lg border border-aegis-border">
              {apiService.getApiBaseUrl()}
            </span>
          </div>

          <div className="flex justify-between items-center text-xs">
            <span className="text-slate-400">Connection Health</span>
            <div className="flex items-center gap-2">
              <span
                className={`w-2.5 h-2.5 rounded-full ${
                  isOk === true ? 'bg-emerald-500' : isOk === false ? 'bg-red-500' : 'bg-amber-400'
                }`}
              />
              <span className="font-semibold text-slate-200">{healthStatus}</span>
            </div>
          </div>
        </div>

        <button
          onClick={testConnection}
          disabled={testing}
          className="px-4 py-2 rounded-xl bg-purple-gradient text-xs font-bold text-white shadow-glow-sm flex items-center gap-2"
        >
          <RefreshCw className={`w-4 h-4 ${testing ? 'animate-spin' : ''}`} />
          <span>Run API Health Diagnostic</span>
        </button>
      </div>

      {/* MARKET PREFERENCES PANEL */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <h3 className="font-bold text-white text-base flex items-center gap-2">
          <Sliders className="w-5 h-5 text-aegis-secondary" />
          Default Market Preferences
        </h3>

        <div className="space-y-4 text-xs">
          <div className="flex justify-between items-center py-2 border-b border-aegis-border/40">
            <div>
              <p className="font-semibold text-white">Default Ticker Symbol</p>
              <p className="text-slate-400 text-[11px]">Primary symbol loaded on launch</p>
            </div>
            <select
              value={symbol}
              onChange={e => onSymbolChange(e.target.value)}
              className="bg-aegis-card border border-aegis-border px-3 py-1.5 rounded-xl font-bold text-white focus:outline-none cursor-pointer"
            >
              {availableSymbols.map(s => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* ACCOUNT INFO */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <h3 className="font-bold text-white text-base flex items-center gap-2">
          <User className="w-5 h-5 text-aegis-ai" />
          Account & Workspace
        </h3>
        <div className="p-4 rounded-xl bg-aegis-bg-subtle border border-aegis-border text-xs space-y-2">
          <div className="flex justify-between">
            <span className="text-slate-400">Authenticated User</span>
            <span className="font-bold text-white">Demo Account</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Role</span>
            <span className="font-semibold text-aegis-primary-bright">Quantitative Analyst</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">ML Model Version</span>
            <span className="font-mono text-slate-300">mvp_v1</span>
          </div>
        </div>
      </div>
    </div>
  );
};
