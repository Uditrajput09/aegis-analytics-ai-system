import React, { useState, useEffect } from 'react';
import { AppLayout } from './layouts/AppLayout';
import type { PageId } from './layouts/AppLayout';
import { LoginPage } from './pages/LoginPage';
import { OverviewPage } from './pages/OverviewPage';
import { InsightsPage } from './pages/InsightsPage';
import { MarketAnalyticsPage } from './pages/MarketAnalyticsPage';
import { ForecastsPage } from './pages/ForecastsPage';
import { RiskAnalyticsPage } from './pages/RiskAnalyticsPage';
import { BlockchainAuditPage } from './pages/BlockchainAuditPage';
import { CryptoDefiPage } from './pages/CryptoDefiPage';
import { WatchlistPage } from './pages/WatchlistPage';
import { AIAnalystPage } from './pages/AIAnalystPage';
import { ReportsPage } from './pages/ReportsPage';
import { SettingsPage } from './pages/SettingsPage';
import { apiService } from './services/api';
import type { User } from './types/api';

export const App: React.FC = () => {
  const [user, setUser] = useState<User | null>(() => apiService.getStoredUser());
  const [currentPage, setCurrentPage] = useState<PageId>('overview');
  const [selectedSymbol, setSelectedSymbol] = useState<string>('RELIANCE.NS');
  const [availableSymbols, setAvailableSymbols] = useState<string[]>([
    'RELIANCE.NS',
    'INFY.NS',
    'TCS.NS',
    'AAPL',
    'GOOGL',
    'MSFT',
  ]);

  useEffect(() => {
    let mounted = true;
    apiService
      .getSymbols()
      .then(symbols => {
        if (mounted && symbols.length > 0) {
          setAvailableSymbols(symbols);
          if (!symbols.includes(selectedSymbol)) {
            setSelectedSymbol(symbols[0]);
          }
        }
      })
      .catch(err => {
        console.warn('Using default symbols list:', err);
      });
    return () => {
      mounted = false;
    };
  }, []);

  const handleSignOut = () => {
    apiService.clearStoredUser();
    setUser(null);
    setCurrentPage('overview');
  };

  if (!user) {
    return <LoginPage onLoginSuccess={setUser} />;
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'overview':
        return (
          <OverviewPage
            symbol={selectedSymbol}
            onSymbolChange={setSelectedSymbol}
            availableSymbols={availableSymbols}
          />
        );
      case 'insights':
        return <InsightsPage symbol={selectedSymbol} />;
      case 'analytics':
        return <MarketAnalyticsPage symbol={selectedSymbol} />;
      case 'forecasts':
        return <ForecastsPage symbol={selectedSymbol} />;
      case 'risk':
        return <RiskAnalyticsPage symbol={selectedSymbol} />;
      case 'blockchain':
        return <BlockchainAuditPage symbol={selectedSymbol} />;
      case 'crypto':
        return <CryptoDefiPage />;
      case 'watchlist':
        return (
          <WatchlistPage
            onSelectSymbol={sym => {
              setSelectedSymbol(sym);
              setCurrentPage('overview');
            }}
          />
        );
      case 'analyst':
        return <AIAnalystPage symbol={selectedSymbol} onNavigate={setCurrentPage} />;
      case 'reports':
        return <ReportsPage symbol={selectedSymbol} />;
      case 'settings':
        return (
          <SettingsPage
            symbol={selectedSymbol}
            onSymbolChange={setSelectedSymbol}
            availableSymbols={availableSymbols}
          />
        );
      default:
        return (
          <OverviewPage
            symbol={selectedSymbol}
            onSymbolChange={setSelectedSymbol}
            availableSymbols={availableSymbols}
          />
        );
    }
  };

  return (
    <AppLayout
      currentPage={currentPage}
      onNavigate={setCurrentPage}
      selectedSymbol={selectedSymbol}
      onSymbolChange={setSelectedSymbol}
      availableSymbols={availableSymbols}
      user={user}
      onSignOut={handleSignOut}
    >
      {renderPage()}
    </AppLayout>
  );
};

export default App;
