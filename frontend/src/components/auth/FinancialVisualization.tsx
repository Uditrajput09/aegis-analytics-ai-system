import React from 'react';

export const FinancialVisualization: React.FC = () => {
  return (
    <div className="relative w-full max-w-lg select-none perspective-1000">
      {/* Background Ambient Glow Orbs */}
      <div className="absolute -top-10 -left-10 w-72 h-72 bg-violet-600/25 rounded-full blur-[80px] pointer-events-none animate-pulse" />
      <div className="absolute -bottom-10 -right-10 w-72 h-72 bg-purple-500/20 rounded-full blur-[80px] pointer-events-none" />

      {/* Glass Card Container */}
      <div className="relative backdrop-blur-xl bg-[rgba(15,10,30,0.75)] border border-violet-500/25 rounded-3xl p-6 shadow-[0_20px_50px_rgba(8,3,15,0.7)] hover:border-violet-500/40 transition-all duration-500 group overflow-hidden">
        {/* Subtle grid pattern overlay */}
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(124,58,237,0.12),transparent_70%)] pointer-events-none" />
        <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-violet-500/10 to-transparent rounded-bl-full pointer-events-none" />

        {/* Top Header Row */}
        <div className="flex items-center justify-between mb-5 relative z-10">
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 rounded-full bg-emerald-400 animate-ping" />
            <div className="flex flex-col">
              <span className="text-xs font-semibold uppercase tracking-wider text-violet-300/80">
                AI Predictive Signal
              </span>
              <span className="text-sm font-bold text-white flex items-center gap-1.5">
                NIFTY 50 / NASDAQ <span className="text-xs font-normal text-emerald-400 font-mono">↗ +1.84%</span>
              </span>
            </div>
          </div>
          <span className="px-3 py-1 rounded-full text-xs font-medium bg-violet-500/15 text-violet-300 border border-violet-500/30 flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-violet-400 animate-pulse" />
            Live Forecast
          </span>
        </div>

        {/* Floating Mini Metric Strip */}
        <div className="grid grid-cols-3 gap-2.5 mb-5 relative z-10">
          <div className="bg-purple-950/40 border border-purple-500/20 rounded-xl p-2.5 flex flex-col">
            <span className="text-[10px] uppercase tracking-wider font-semibold text-purple-300/70">
              Confidence
            </span>
            <span className="text-base font-bold font-mono text-violet-200">92.4%</span>
          </div>
          <div className="bg-purple-950/40 border border-purple-500/20 rounded-xl p-2.5 flex flex-col">
            <span className="text-[10px] uppercase tracking-wider font-semibold text-purple-300/70">
              Tail Risk
            </span>
            <span className="text-base font-bold font-mono text-emerald-400">Low (1.8%)</span>
          </div>
          <div className="bg-purple-950/40 border border-purple-500/20 rounded-xl p-2.5 flex flex-col">
            <span className="text-[10px] uppercase tracking-wider font-semibold text-purple-300/70">
              Exp Return
            </span>
            <span className="text-base font-bold font-mono text-purple-300">+3.45%</span>
          </div>
        </div>

        {/* SVG Decorative Trend & Prediction Band Graph */}
        <div className="relative h-40 w-full overflow-hidden rounded-xl bg-purple-950/30 border border-violet-500/15 p-2 flex items-end">
          <svg className="w-full h-full overflow-visible" viewBox="0 0 400 120" preserveAspectRatio="none">
            <defs>
              <linearGradient id="chartGlow" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#8B5CF6" stopOpacity="0.45" />
                <stop offset="100%" stopColor="#7C3AED" stopOpacity="0.0" />
              </linearGradient>
              <linearGradient id="lineGrad" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stopColor="#6366F1" />
                <stop offset="50%" stopColor="#8B5CF6" />
                <stop offset="100%" stopColor="#EC4899" />
              </linearGradient>
            </defs>

            {/* Prediction interval band */}
            <path
              d="M 0 80 Q 100 65 200 50 T 400 20 L 400 60 Q 300 80 200 85 T 0 105 Z"
              fill="rgba(139, 92, 246, 0.12)"
            />

            {/* Grid lines */}
            <line x1="0" y1="30" x2="400" y2="30" stroke="rgba(255,255,255,0.05)" strokeDasharray="4 4" />
            <line x1="0" y1="60" x2="400" y2="60" stroke="rgba(255,255,255,0.05)" strokeDasharray="4 4" />
            <line x1="0" y1="90" x2="400" y2="90" stroke="rgba(255,255,255,0.05)" strokeDasharray="4 4" />

            {/* Main Area Fill */}
            <path
              d="M 0 95 Q 60 70 120 75 T 240 45 T 360 25 L 400 20 L 400 120 L 0 120 Z"
              fill="url(#chartGlow)"
            />

            {/* Main Trend Line */}
            <path
              d="M 0 95 Q 60 70 120 75 T 240 45 T 360 25 L 400 20"
              fill="none"
              stroke="url(#lineGrad)"
              strokeWidth="3.5"
              strokeLinecap="round"
            />

            {/* Active prediction node pulse */}
            <circle cx="360" cy="25" r="5" fill="#F472B6" />
            <circle cx="360" cy="25" r="9" fill="none" stroke="#F472B6" strokeWidth="1.5" className="animate-ping origin-center" />
          </svg>

          {/* Floating AI Callout Overlay */}
          <div className="absolute top-3 right-4 backdrop-blur-md bg-purple-900/60 border border-purple-400/30 rounded-lg px-2.5 py-1 text-[11px] font-medium text-purple-200 shadow-lg flex items-center gap-1.5">
            <span className="text-pink-400 font-bold">✨ AI Insight:</span> Outperforming Sector
          </div>
        </div>

        {/* Footer Subtext */}
        <div className="mt-4 flex items-center justify-between text-xs text-violet-300/60 relative z-10">
          <span className="flex items-center gap-1">
            <svg className="w-3.5 h-3.5 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Real-time Conformal Analytics
          </span>
          <span className="font-mono text-[11px]">90% Coverage Guarantee</span>
        </div>
      </div>
    </div>
  );
};
