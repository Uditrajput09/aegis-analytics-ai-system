import React from 'react';
import { HeroSection } from '../components/auth/HeroSection';
import { LoginCard } from '../components/auth/LoginCard';
import type { User } from '../types/api';

interface LoginPageProps {
  onLoginSuccess: (user: User) => void;
}

export const LoginPage: React.FC<LoginPageProps> = ({ onLoginSuccess }) => {
  return (
    <div className="min-h-screen w-full bg-[#08030F] text-slate-100 flex items-center justify-center p-4 sm:p-6 lg:p-12 relative overflow-hidden font-sans">
      {/* Background Animated Gradient Atmosphere */}
      <div className="absolute top-0 left-1/4 w-[600px] h-[600px] bg-gradient-to-br from-violet-700/20 to-purple-900/10 rounded-full blur-[140px] pointer-events-none animate-pulse" />
      <div className="absolute bottom-0 right-1/4 w-[600px] h-[600px] bg-gradient-to-tr from-indigo-700/15 to-purple-800/10 rounded-full blur-[140px] pointer-events-none" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-purple-950/10 rounded-full blur-[160px] pointer-events-none" />

      {/* Decorative Grid Mesh */}
      <div 
        className="absolute inset-0 opacity-[0.03] pointer-events-none" 
        style={{
          backgroundImage: `radial-gradient(circle at 1px 1px, rgba(255, 255, 255, 0.4) 1px, transparent 0)`,
          backgroundSize: '32px 32px'
        }}
      />

      {/* Main Container */}
      <div className="relative z-10 w-full max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
        {/* Left Hero Section (7 cols on desktop) */}
        <div className="lg:col-span-7 flex flex-col justify-center">
          <HeroSection />
        </div>

        {/* Right Login Card Section (5 cols on desktop) */}
        <div className="lg:col-span-5 flex items-center justify-center w-full mt-4 lg:mt-0">
          <LoginCard onSuccess={onLoginSuccess} />
        </div>
      </div>
    </div>
  );
};
