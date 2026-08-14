import React, { useState, useEffect } from 'react';
import { FileText, Share2, Printer } from 'lucide-react';
import { apiService } from '../services/api';
import type { PredictionLatest, RiskLatest, AIInsight } from '../types/api';

interface ReportsPageProps {
  symbol: string;
}

export const ReportsPage: React.FC<ReportsPageProps> = ({ symbol }) => {
  const [prediction, setPrediction] = useState<PredictionLatest | null>(null);
  const [risk, setRisk] = useState<RiskLatest | null>(null);

  const loadReportData = async () => {
    try {
      const [p, r] = await Promise.all([
        apiService.getLatestPrediction(symbol, '5m', '1m'),
        apiService.getLatestRisk(symbol, '5m', '1m'),
      ]);
      setPrediction(p);
      setRisk(r);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadReportData();
  }, [symbol]);

  const insights: AIInsight[] = prediction && risk ? apiService.deriveAIInsights(prediction, risk) : [];
  const signal = prediction && risk ? apiService.deriveSignal(prediction, risk) : null;

  return (
    <div className="space-y-6 pb-12">
      {/* HEADER ACTIONS */}
      <div className="glass-panel p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <FileText className="w-6 h-6 text-aegis-primary-bright" />
            Executive Intelligence Report
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Quantitative analysis report generated for{' '}
            <span className="text-aegis-primary-bright font-bold">{symbol}</span> on{' '}
            {new Date().toLocaleDateString()}.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => window.print()}
            className="px-4 py-2 rounded-xl glass-panel text-xs font-semibold text-slate-200 hover:text-white flex items-center gap-2"
          >
            <Printer className="w-4 h-4" />
            <span>Print / PDF</span>
          </button>
          <button className="px-4 py-2 rounded-xl bg-purple-gradient text-xs font-bold text-white shadow-glow-sm flex items-center gap-2">
            <Share2 className="w-4 h-4" />
            <span>Share Report</span>
          </button>
        </div>
      </div>

      {/* REPORT BODY DOCUMENT CONTAINER */}
      <div className="glass-panel p-8 rounded-2xl space-y-8 border border-aegis-border/60">
        {/* EXECUTIVE SUMMARY */}
        <div className="border-b border-aegis-border/40 pb-6">
          <span className="text-xs font-bold uppercase tracking-widest text-aegis-primary-bright">
            Section 1: Executive Summary
          </span>
          <h2 className="text-xl font-bold text-white mt-1">Market Outlook & Model Signals</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
            <div className="p-4 rounded-xl bg-aegis-bg-subtle border border-aegis-border">
              <span className="text-xs text-slate-400">Target Asset</span>
              <p className="text-lg font-extrabold text-white">{symbol}</p>
            </div>
            <div className="p-4 rounded-xl bg-aegis-bg-subtle border border-aegis-border">
              <span className="text-xs text-slate-400">Current Signal</span>
              <p className="text-lg font-extrabold text-aegis-positive">{signal?.label || '---'}</p>
            </div>
            <div className="p-4 rounded-xl bg-aegis-bg-subtle border border-aegis-border">
              <span className="text-xs text-slate-400">Expected 5m Return</span>
              <p className="text-lg font-extrabold text-white">
                {prediction ? `+${(prediction.expected_return * 100).toFixed(2)}%` : '---'}
              </p>
            </div>
          </div>
        </div>

        {/* QUANTITATIVE PREDICTIONS */}
        <div className="border-b border-aegis-border/40 pb-6">
          <span className="text-xs font-bold uppercase tracking-widest text-aegis-primary-bright">
            Section 2: Key Predictions
          </span>
          <h2 className="text-xl font-bold text-white mt-1">LightGBM Forecast Telemetry</h2>
          <p className="text-sm text-slate-300 mt-2">
            The dual-head model projects a target price of{' '}
            <strong className="text-white">₹{prediction?.expected_price?.toFixed(2)}</strong> from last
            close ₹{prediction?.last_close?.toFixed(2)}. Isotonic directional classification indicates a{' '}
            <strong className="text-aegis-ai">
              {prediction?.p_up ? `${(prediction.p_up * 100).toFixed(1)}%` : 'N/A'}
            </strong>{' '}
            probability of upward movement.
          </p>
        </div>

        {/* RISK ASSESSMENT */}
        <div className="border-b border-aegis-border/40 pb-6">
          <span className="text-xs font-bold uppercase tracking-widest text-aegis-risk">
            Section 3: Downside Tail Risk
          </span>
          <h2 className="text-xl font-bold text-white mt-1">Conformal Interval Analysis</h2>
          <p className="text-sm text-slate-300 mt-2">
            Statistical 90% conformal prediction bounds span from{' '}
            <strong className="text-red-400">
              {(prediction?.interval_low || 0) * 100}%
            </strong>{' '}
            to{' '}
            <strong className="text-emerald-400">
              +{(prediction?.interval_high || 0) * 100}%
            </strong>
            . Downside probability of a &gt;2% loss event is evaluated at{' '}
            <strong className="text-aegis-risk">
              {risk ? `${(risk.p_return_below_minus_2pct * 100).toFixed(1)}%` : '---'}
            </strong>
            .
          </p>
        </div>

        {/* AI INSIGHTS SUMMARY */}
        <div>
          <span className="text-xs font-bold uppercase tracking-widest text-aegis-primary-bright">
            Section 4: AI Insights Summary
          </span>
          <h2 className="text-xl font-bold text-white mt-1">Key Actionable Findings</h2>
          <div className="space-y-3 mt-4">
            {insights.map(i => (
              <div key={i.id} className="p-4 rounded-xl bg-aegis-bg-subtle border border-aegis-border">
                <span className="text-xs font-bold text-aegis-primary-bright">{i.category}</span>
                <h4 className="font-bold text-white text-sm mt-0.5">{i.title}</h4>
                <p className="text-xs text-slate-400 mt-1">{i.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
