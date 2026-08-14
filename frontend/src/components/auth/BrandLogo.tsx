import React from 'react';

interface BrandLogoProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const BrandLogo: React.FC<BrandLogoProps> = ({ size = 'md', className = '' }) => {
  const iconSizes = {
    sm: 'w-7 h-7',
    md: 'w-9 h-9',
    lg: 'w-12 h-12',
  };

  const titleSizes = {
    sm: 'text-lg',
    md: 'text-xl',
    lg: 'text-2xl',
  };

  return (
    <div className={`flex items-center gap-3 select-none ${className}`}>
      {/* Modern Shield + AI Node Icon */}
      <div className={`relative flex items-center justify-center rounded-xl bg-gradient-to-br from-violet-600/30 via-purple-600/20 to-indigo-900/40 p-2 border border-violet-500/30 shadow-[0_0_20px_rgba(139,92,246,0.3)] ${iconSizes[size]}`}>
        <svg viewBox="0 0 24 24" fill="none" className="w-full h-full text-violet-400 drop-shadow-[0_0_8px_rgba(167,139,250,0.8)]" stroke="currentColor" strokeWidth="2">
          <path d="M12 2L3 6v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-5.45 9-12V6l-9-4z" fill="url(#shield-grad)" fillOpacity="0.2" stroke="currentColor" />
          <path d="M7 14l3-3 2.5 2.5L17 9" stroke="#A78BFA" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          <circle cx="17" cy="9" r="1.5" fill="#F472B6" />
          <circle cx="7" cy="14" r="1.5" fill="#63B3ED" />
          <defs>
            <linearGradient id="shield-grad" x1="0" y1="0" x2="24" y2="24">
              <stop offset="0%" stopColor="#8B5CF6" />
              <stop offset="100%" stopColor="#3B82F6" />
            </linearGradient>
          </defs>
        </svg>
      </div>

      <div className="flex flex-col">
        <div className={`font-bold tracking-tight text-white flex items-center gap-1.5 ${titleSizes[size]}`}>
          <span>AEGIS</span>
          <span className="bg-gradient-to-r from-violet-400 via-purple-300 to-indigo-300 bg-clip-text text-transparent font-extrabold">
            ANALYTICS
          </span>
        </div>
        <span className="text-[10px] tracking-[0.22em] uppercase font-semibold text-violet-300/60 -mt-1">
          AI Intelligence
        </span>
      </div>
    </div>
  );
};
