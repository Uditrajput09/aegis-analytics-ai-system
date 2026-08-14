import React from 'react';
import { BrandLogo } from './BrandLogo';
import { FinancialVisualization } from './FinancialVisualization';

export const HeroSection: React.FC = () => {
  return (
    <div className="flex flex-col justify-between h-full max-w-xl pr-0 lg:pr-8 py-2">
      {/* Top Brand Logo */}
      <div className="mb-8 lg:mb-12">
        <BrandLogo size="lg" />
      </div>

      {/* Hero Headline & Intro */}
      <div className="space-y-6 my-auto">
        <h1 className="text-4xl lg:text-5xl xl:text-6xl font-extrabold text-white leading-[1.15] tracking-tight">
          Intelligence for <br />
          <span className="bg-gradient-to-r from-violet-400 via-purple-400 to-indigo-400 bg-clip-text text-transparent drop-shadow-[0_0_25px_rgba(139,92,246,0.4)]">
            every market decision.
          </span>
        </h1>

        <p className="text-base lg:text-lg text-violet-200/70 leading-relaxed max-w-lg">
          Turn market data into actionable intelligence with AI-powered predictions, conformal risk analytics, and intelligent market forecasts.
        </p>

        {/* Feature Highlights Strip */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2">
          <div className="flex items-center gap-2.5 p-3 rounded-xl bg-purple-950/40 border border-violet-500/20 backdrop-blur-sm">
            <span className="flex items-center justify-center w-8 h-8 rounded-lg bg-violet-500/20 text-violet-300 text-sm">⚡</span>
            <div className="flex flex-col">
              <span className="text-xs font-bold text-white">AI Predictions</span>
              <span className="text-[10px] text-violet-300/60">Multi-horizon</span>
            </div>
          </div>

          <div className="flex items-center gap-2.5 p-3 rounded-xl bg-purple-950/40 border border-violet-500/20 backdrop-blur-sm">
            <span className="flex items-center justify-center w-8 h-8 rounded-lg bg-purple-500/20 text-purple-300 text-sm">🛡️</span>
            <div className="flex flex-col">
              <span className="text-xs font-bold text-white">Risk Intelligence</span>
              <span className="text-[10px] text-violet-300/60">Conformal bounds</span>
            </div>
          </div>

          <div className="flex items-center gap-2.5 p-3 rounded-xl bg-purple-950/40 border border-violet-500/20 backdrop-blur-sm">
            <span className="flex items-center justify-center w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-300 text-sm">📊</span>
            <div className="flex flex-col">
              <span className="text-xs font-bold text-white">Market Signals</span>
              <span className="text-[10px] text-violet-300/60">Real-time data</span>
            </div>
          </div>
        </div>

        {/* Decorative Financial Panel */}
        <div className="pt-6 hidden sm:block">
          <FinancialVisualization />
        </div>
      </div>

      {/* Bottom Brand Signature */}
      <div className="mt-8 text-xs text-violet-400/50 flex items-center gap-2">
        <span className="w-1.5 h-1.5 rounded-full bg-violet-500" />
        <span>Powered by Aegis Analytics AI &bull; Quantitative Intelligence Engine</span>
      </div>
    </div>
  );
};
