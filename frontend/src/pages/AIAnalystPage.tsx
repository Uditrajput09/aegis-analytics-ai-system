import React, { useState, useEffect, useRef } from 'react';
import { Bot, Send, User as UserIcon, Sparkles, ChevronRight } from 'lucide-react';
import { apiService } from '../services/api';
import type { PredictionLatest, RiskLatest, AIChatMessage } from '../types/api';

interface AIAnalystPageProps {
  symbol: string;
  onNavigate: (page: any) => void;
}

export const AIAnalystPage: React.FC<AIAnalystPageProps> = ({ symbol, onNavigate }) => {
  const [horizon] = useState<'5m' | '15m' | '60m' | '1d'>('5m');
  const [prediction, setPrediction] = useState<PredictionLatest | null>(null);
  const [risk, setRisk] = useState<RiskLatest | null>(null);
  const [inputQuery, setInputQuery] = useState('');
  const [messages, setMessages] = useState<AIChatMessage[]>([]);
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef<HTMLDivElement>(null);

  const loadContext = async () => {
    try {
      const tf = horizon === '1d' ? '1d' : '1m';
      const [p, r] = await Promise.all([
        apiService.getLatestPrediction(symbol, horizon, tf),
        apiService.getLatestRisk(symbol, horizon, tf),
      ]);
      setPrediction(p);
      setRisk(r);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadContext();
  }, [symbol, horizon]);

  // Initial welcome message
  useEffect(() => {
    setMessages([
      {
        id: '1',
        sender: 'assistant',
        text: `Hello! I am **Aegis AI Analyst**, your quantitative financial intelligence co-pilot. I have loaded live predictions for **${symbol}** (${horizon} horizon).\n\nAsk me about current directional outlook, risk probabilities, multi-horizon comparison, or strategy rules!`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      },
    ]);
  }, [symbol, horizon]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = (textToSend?: string) => {
    const q = textToSend || inputQuery;
    if (!q.trim() || !prediction || !risk) return;

    const userMsg: AIChatMessage = {
      id: Date.now().toString(),
      sender: 'user',
      text: q,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages(prev => [...prev, userMsg]);
    if (!textToSend) setInputQuery('');
    setLoading(true);

    setTimeout(() => {
      const signal = apiService.deriveSignal(prediction, risk);
      let replyText = '';

      const queryLower = q.toLowerCase();

      if (queryLower.includes('outlook') || queryLower.includes('prediction') || queryLower.includes('current')) {
        replyText = `**Current Outlook for ${symbol} (${horizon}):**\n\n- **Signal:** ${signal.label}\n- **Expected Return:** +${(prediction.expected_return * 100).toFixed(2)}%\n- **Target Price:** ₹${prediction.expected_price.toFixed(2)} (Last close: ₹${prediction.last_close.toFixed(2)})\n- **P(Up):** ${prediction.p_up ? `${(prediction.p_up * 100).toFixed(1)}%` : 'N/A'}\n- **90% Range:** ${(prediction.interval_low * 100).toFixed(2)}% to +${(prediction.interval_high * 100).toFixed(2)}%\n\n${signal.reason}`;
      } else if (queryLower.includes('risk') || queryLower.includes('downside')) {
        replyText = `**Risk Telemetry for ${symbol}:**\n\n- **P(Return < -1%):** ${(risk.p_return_below_minus_1pct * 100).toFixed(1)}%\n- **P(Return < -2%):** ${(risk.p_return_below_minus_2pct * 100).toFixed(1)}%\n- **Conformal Interval Width:** ${Math.abs(prediction.interval_high - prediction.interval_low) * 100}%`;
      } else if (queryLower.includes('horizon') || queryLower.includes('compare')) {
        replyText = `**Multi-Horizon Overview:**\n\nYou are viewing the **${horizon}** horizon. Use the **Forecasts** page to view side-by-side matrices comparing 5m, 15m, 60m, and 1d return vectors.`;
      } else {
        replyText = `Based on the latest model telemetry for **${symbol}**, expected return is **${(prediction.expected_return * 100).toFixed(2)}%** with a **${signal.label}** classification.`;
      }

      const botMsg: AIChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: replyText,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages(prev => [...prev, botMsg]);
      setLoading(false);
    }, 600);
  };

  const suggestedQuestions = [
    'What is the current outlook?',
    'Explain the downside risk',
    'Which horizon looks strongest?',
    'What does the prediction interval mean?',
  ];

  return (
    <div className="h-[calc(100vh-7rem)] flex flex-col lg:flex-row gap-6 pb-6">
      {/* LEFT / MAIN CONVERSATION PANEL */}
      <div className="flex-1 glass-panel rounded-2xl flex flex-col overflow-hidden">
        {/* CHAT HEADER */}
        <div className="p-4 border-b border-aegis-border/50 flex items-center justify-between bg-aegis-card/50">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-purple-gradient flex items-center justify-center text-white shadow-glow-purple">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <h2 className="font-bold text-white text-base">Ask Aegis — AI Market Copilot</h2>
              <p className="text-[10px] text-slate-400">Powered by Aegis Quantitative Inference Engine</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => onNavigate('forecasts')}
              className="px-3 py-1.5 rounded-xl bg-aegis-bg-subtle border border-aegis-border text-xs font-semibold text-slate-300 hover:text-white"
            >
              View Forecasts
            </button>
            <button
              onClick={() => onNavigate('reports')}
              className="px-3 py-1.5 rounded-xl bg-purple-gradient text-xs font-bold text-white shadow-glow-sm"
            >
              Generate Report
            </button>
          </div>
        </div>

        {/* CHAT MESSAGES STREAM */}
        <div className="flex-1 p-6 overflow-y-auto space-y-4">
          {messages.map(msg => (
            <div
              key={msg.id}
              className={`flex gap-3 max-w-2xl ${
                msg.sender === 'user' ? 'ml-auto flex-row-reverse' : ''
              }`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 ${
                  msg.sender === 'user'
                    ? 'bg-aegis-secondary text-white'
                    : 'bg-aegis-primary text-white shadow-glow-purple'
                }`}
              >
                {msg.sender === 'user' ? <UserIcon className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>
              <div
                className={`p-4 rounded-2xl text-sm leading-relaxed ${
                  msg.sender === 'user'
                    ? 'bg-aegis-secondary text-white rounded-tr-none'
                    : 'glass-panel text-slate-200 rounded-tl-none border-aegis-border'
                }`}
              >
                <div className="whitespace-pre-line">{msg.text}</div>
                <div className="text-[10px] opacity-50 mt-2 text-right">{msg.timestamp}</div>
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex items-center gap-2 text-xs text-aegis-ai animate-pulse">
              <Bot className="w-4 h-4" />
              <span>Aegis is analyzing market telemetry...</span>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        {/* SUGGESTED QUESTIONS CHIPS */}
        <div className="px-4 py-2 bg-aegis-card/30 border-t border-aegis-border/30 flex items-center gap-2 overflow-x-auto">
          {suggestedQuestions.map((q, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(q)}
              className="px-3 py-1.5 rounded-full bg-aegis-bg-subtle border border-aegis-border/60 hover:border-aegis-primary-bright text-xs text-slate-300 hover:text-white whitespace-nowrap transition-colors"
            >
              {q}
            </button>
          ))}
        </div>

        {/* INPUT FORM */}
        <div className="p-4 border-t border-aegis-border/50 bg-aegis-card/80">
          <form
            onSubmit={e => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center gap-3"
          >
            <input
              type="text"
              placeholder="Ask Aegis about forecasts, risk, or horizon strategy..."
              value={inputQuery}
              onChange={e => setInputQuery(e.target.value)}
              className="flex-1 bg-aegis-bg-subtle border border-aegis-border rounded-xl px-4 py-3 text-sm text-white placeholder-slate-400 focus:outline-none focus:border-aegis-primary-bright"
            />
            <button
              type="submit"
              disabled={!inputQuery.trim() || loading}
              className="p-3 rounded-xl bg-purple-gradient text-white shadow-glow-purple hover:opacity-90 disabled:opacity-40 transition-all"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>

      {/* RIGHT LIVE MARKET CONTEXT SIDEBAR */}
      <div className="w-full lg:w-80 glass-panel p-5 rounded-2xl space-y-4">
        <h3 className="font-bold text-white text-sm flex items-center gap-2 border-b border-aegis-border/50 pb-3">
          <Sparkles className="w-4 h-4 text-aegis-ai" />
          Live Market Context
        </h3>

        <div className="space-y-3 text-xs">
          <div className="flex justify-between py-1 border-b border-white/5">
            <span className="text-slate-400">Active Symbol</span>
            <span className="font-extrabold text-aegis-primary-bright">{symbol}</span>
          </div>

          <div className="flex justify-between py-1 border-b border-white/5">
            <span className="text-slate-400">Horizon</span>
            <span className="font-semibold text-white">{horizon}</span>
          </div>

          <div className="flex justify-between py-1 border-b border-white/5">
            <span className="text-slate-400">Last Close</span>
            <span className="font-semibold text-white">
              ₹{prediction?.last_close?.toFixed(2) || '---'}
            </span>
          </div>

          <div className="flex justify-between py-1 border-b border-white/5">
            <span className="text-slate-400">Expected Return</span>
            <span
              className={`font-bold ${
                (prediction?.expected_return || 0) >= 0 ? 'text-aegis-positive' : 'text-aegis-risk'
              }`}
            >
              {prediction ? `${(prediction.expected_return * 100).toFixed(2)}%` : '---'}
            </span>
          </div>

          <div className="flex justify-between py-1 border-b border-white/5">
            <span className="text-slate-400">Probability Up</span>
            <span className="font-bold text-aegis-ai">
              {prediction?.p_up ? `${(prediction.p_up * 100).toFixed(1)}%` : '---'}
            </span>
          </div>

          <div className="flex justify-between py-1 border-b border-white/5">
            <span className="text-slate-400">P(Return &lt; -2%)</span>
            <span className="font-bold text-aegis-risk">
              {risk ? `${(risk.p_return_below_minus_2pct * 100).toFixed(1)}%` : '---'}
            </span>
          </div>
        </div>

        <div className="pt-2">
          <button
            onClick={() => onNavigate('overview')}
            className="w-full py-2.5 rounded-xl bg-aegis-bg-subtle border border-aegis-border text-xs font-semibold text-slate-300 hover:text-white flex items-center justify-center gap-1"
          >
            <span>Open Overview Panel</span>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
