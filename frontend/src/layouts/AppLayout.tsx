import React, { useState, useEffect } from 'react';
import {
  LayoutDashboard,
  Sparkles,
  TrendingUp,
  LineChart,
  ShieldAlert,
  Bookmark,
  Bot,
  FileText,
  Settings as SettingsIcon,
  Search,
  Bell,
  Cpu,
  ChevronLeft,
  ChevronRight,
  Activity,
  AlertTriangle,
  User as UserIcon,
} from 'lucide-react';
import { apiService } from '../services/api';

export type PageId =
  | 'overview'
  | 'insights'
  | 'analytics'
  | 'forecasts'
  | 'risk'
  | 'watchlist'
  | 'analyst'
  | 'reports'
  | 'settings';

interface NavItemDef {
  id: PageId;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: string;
}

interface AppLayoutProps {
  currentPage: PageId;
  onNavigate: (page: PageId) => void;
  selectedSymbol: string;
  onSymbolChange: (symbol: string) => void;
  availableSymbols: string[];
  user?: { id: number; username: string } | null;
  onSignOut?: () => void;
  children: React.ReactNode;
}

export const AppLayout: React.FC<AppLayoutProps> = ({
  currentPage,
  onNavigate,
  selectedSymbol,
  onSymbolChange,
  availableSymbols,
  user,
  onSignOut,
  children,
}) => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [isBackendOnline, setIsBackendOnline] = useState<boolean | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    let mounted = true;
    const checkHealth = async () => {
      try {
        const res = await apiService.getHealth();
        if (mounted) setIsBackendOnline(res.ok);
      } catch {
        if (mounted) setIsBackendOnline(false);
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 15000);
    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  const navItems: NavItemDef[] = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'insights', label: 'AI Insights', icon: Sparkles },
    { id: 'analytics', label: 'Market Analytics', icon: TrendingUp },
    { id: 'forecasts', label: 'Forecasts', icon: LineChart },
    { id: 'risk', label: 'Risk Analytics', icon: ShieldAlert },
    { id: 'watchlist', label: 'Watchlist', icon: Bookmark },
    { id: 'analyst', label: 'AI Analyst', icon: Bot, badge: 'AI' },
    { id: 'reports', label: 'Reports', icon: FileText },
    { id: 'settings', label: 'Settings', icon: SettingsIcon },
  ];

  const filteredSymbols = availableSymbols.filter(s =>
    s.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="min-h-screen flex bg-aegis-bg text-aegis-text">
      {/* LEFT SIDEBAR */}
      <aside
        className={`fixed top-0 left-0 bottom-0 z-40 flex flex-col glass-panel border-r border-aegis-border transition-all duration-300 ${
          sidebarCollapsed ? 'w-20' : 'w-64'
        }`}
      >
        {/* LOGO */}
        <div className="h-20 flex items-center justify-between px-5 border-b border-aegis-border/50">
          <div
            className="flex items-center gap-3 cursor-pointer"
            onClick={() => onNavigate('overview')}
          >
            <div className="w-10 h-10 rounded-xl bg-purple-gradient flex items-center justify-center shadow-glow-purple">
              <Cpu className="w-5 h-5 text-white" />
            </div>
            {!sidebarCollapsed && (
              <div>
                <h1 className="font-bold text-lg leading-tight tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-100 to-purple-300">
                  AEGIS
                </h1>
                <p className="text-[10px] uppercase tracking-widest text-aegis-primary-bright font-semibold">
                  Analytics AI
                </p>
              </div>
            )}
          </div>
          <button
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-aegis-card-hover transition-colors"
            title={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {sidebarCollapsed ? (
              <ChevronRight className="w-4 h-4" />
            ) : (
              <ChevronLeft className="w-4 h-4" />
            )}
          </button>
        </div>

        {/* NAVIGATION */}
        <nav className="flex-1 px-3 py-4 space-y-1.5 overflow-y-auto">
          {navItems.map(item => {
            const Icon = item.icon;
            const isActive = currentPage === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onNavigate(item.id)}
                className={`w-full flex items-center gap-3.5 px-3.5 py-3 rounded-xl font-medium text-sm transition-all duration-200 group relative ${
                  isActive
                    ? 'bg-purple-gradient text-white shadow-glow-sm font-semibold'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
                }`}
                title={sidebarCollapsed ? item.label : undefined}
              >
                <Icon
                  className={`w-5 h-5 transition-transform group-hover:scale-110 ${
                    isActive ? 'text-white' : 'text-slate-400 group-hover:text-aegis-primary-bright'
                  }`}
                />
                {!sidebarCollapsed && <span>{item.label}</span>}
                {!sidebarCollapsed && item.badge && (
                  <span className="ml-auto text-[10px] font-bold px-2 py-0.5 rounded-full bg-aegis-ai/30 text-aegis-ai border border-aegis-ai/40">
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* FOOTER & STATUS */}
        <div className="p-4 border-t border-aegis-border/50 space-y-3">
          {!sidebarCollapsed && (
            <div className="p-3 rounded-xl bg-aegis-bg-subtle/80 border border-aegis-border/40 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="relative flex h-2.5 w-2.5">
                  <span
                    className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
                      isBackendOnline ? 'bg-emerald-400' : 'bg-red-400'
                    }`}
                  />
                  <span
                    className={`relative inline-flex rounded-full h-2.5 w-2.5 ${
                      isBackendOnline ? 'bg-emerald-500' : 'bg-red-500'
                    }`}
                  />
                </span>
                <span className="text-xs font-medium text-slate-300">
                  {isBackendOnline === null
                    ? 'Connecting...'
                    : isBackendOnline
                    ? 'AI Engine Online'
                    : 'Backend Offline'}
                </span>
              </div>
              <Activity className="w-3.5 h-3.5 text-aegis-primary-bright" />
            </div>
          )}

          {/* USER PROFILE */}
          <div className="flex items-center justify-between gap-2 pt-1 border-t border-aegis-border/40 mt-2">
            <div className="flex items-center gap-3 overflow-hidden">
              <div className="w-9 h-9 rounded-full bg-violet-600/30 border border-violet-500/40 flex items-center justify-center text-violet-300 font-bold text-xs uppercase shrink-0">
                {user?.username ? user.username.charAt(0) : <UserIcon className="w-4 h-4" />}
              </div>
              {!sidebarCollapsed && (
                <div className="overflow-hidden">
                  <p className="text-xs font-semibold text-white truncate">{user?.username || 'Demo Account'}</p>
                  <p className="text-[10px] text-violet-300/60 truncate">Quantitative Analyst</p>
                </div>
              )}
            </div>
            {!sidebarCollapsed && onSignOut && (
              <button
                onClick={onSignOut}
                title="Sign Out"
                className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition-colors"
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </button>
            )}
          </div>
        </div>
      </aside>

      {/* MAIN CONTAINER */}
      <div
        className={`flex-1 flex flex-col min-w-0 transition-all duration-300 ${
          sidebarCollapsed ? 'ml-20' : 'ml-64'
        }`}
      >
        {/* TOP HEADER */}
        <header className="h-20 sticky top-0 z-30 glass-panel border-b border-aegis-border/50 px-6 flex items-center justify-between gap-4">
          {/* SEARCH BAR */}
          <div className="relative flex-1 max-w-md">
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                placeholder="Search symbols, forecasts, insights..."
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                onFocus={() => setIsSearching(true)}
                onBlur={() => setTimeout(() => setIsSearching(false), 200)}
                className="w-full bg-aegis-bg-subtle border border-aegis-border/60 rounded-xl pl-10 pr-4 py-2 text-sm text-white placeholder-slate-400 focus:outline-none focus:border-aegis-primary-bright focus:ring-1 focus:ring-aegis-primary-bright transition-all"
              />
            </div>

            {/* QUICK SEARCH DROPDOWN */}
            {isSearching && searchQuery.trim() && (
              <div className="absolute top-full mt-2 left-0 right-0 glass-panel rounded-xl border border-aegis-border shadow-glass p-2 space-y-1 z-50 max-h-60 overflow-y-auto">
                {filteredSymbols.length > 0 ? (
                  filteredSymbols.map(sym => (
                    <button
                      key={sym}
                      onClick={() => {
                        onSymbolChange(sym);
                        setSearchQuery('');
                        setIsSearching(false);
                      }}
                      className="w-full text-left px-3 py-2 rounded-lg hover:bg-aegis-card-hover text-sm flex items-center justify-between text-slate-200"
                    >
                      <span className="font-semibold">{sym}</span>
                      <span className="text-xs text-aegis-primary-bright">Select Symbol</span>
                    </button>
                  ))
                ) : (
                  <div className="p-3 text-xs text-slate-400 text-center">
                    No matching symbol found
                  </div>
                )}
              </div>
            )}
          </div>

          {/* RIGHT CONTROLS */}
          <div className="flex items-center gap-4">
            {/* ACTIVE SYMBOL SELECTOR PILL */}
            <div className="flex items-center gap-2 bg-aegis-card/80 border border-aegis-border px-3.5 py-1.5 rounded-xl">
              <span className="text-xs text-slate-400 font-semibold">Active:</span>
              <select
                value={selectedSymbol}
                onChange={e => onSymbolChange(e.target.value)}
                className="bg-transparent text-sm font-bold text-aegis-primary-bright focus:outline-none cursor-pointer"
              >
                {availableSymbols.map(sym => (
                  <option key={sym} value={sym} className="bg-aegis-card text-white">
                    {sym}
                  </option>
                ))}
              </select>
            </div>

            {/* BACKEND OFFLINE BANNER IF OFFLINE */}
            {isBackendOnline === false && (
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-red-500/10 border border-red-500/30 text-aegis-risk text-xs font-semibold">
                <AlertTriangle className="w-4 h-4 animate-bounce" />
                <span>Backend Offline (127.0.0.1:8000)</span>
              </div>
            )}

            {/* NOTIFICATION BUTTON */}
            <button className="p-2.5 rounded-xl glass-panel text-slate-300 hover:text-white hover:border-aegis-primary-bright transition-colors relative">
              <Bell className="w-4 h-4" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-aegis-primary-bright" />
            </button>
          </div>
        </header>

        {/* PAGE CONTENT */}
        <main className="flex-1 p-6 overflow-y-auto">{children}</main>
      </div>
    </div>
  );
};
