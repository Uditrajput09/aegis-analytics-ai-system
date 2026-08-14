import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/api';
import type { User } from '../../types/api';

interface LoginCardProps {
  onSuccess: (user: User) => void;
}

export const LoginCard: React.FC<LoginCardProps> = ({ onSuccess }) => {
  const [isRegisterMode, setIsRegisterMode] = useState<boolean>(false);
  const [username, setUsername] = useState<string>('demo');
  const [password, setPassword] = useState<string>('demo123');
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [rememberMe, setRememberMe] = useState<boolean>(true);

  const [loading, setLoading] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const [systemOnline, setSystemOnline] = useState<boolean | null>(null);

  // Dynamic Health Check on mount
  useEffect(() => {
    let active = true;
    apiService
      .getHealth()
      .then(res => {
        if (active) {
          setSystemOnline(Boolean(res.ok));
        }
      })
      .catch(() => {
        if (active) {
          setSystemOnline(false);
        }
      });
    return () => {
      active = false;
    };
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setSuccessMsg(null);

    const cleanUser = username.trim();
    if (!cleanUser) {
      setErrorMsg('Please enter your email or username.');
      return;
    }
    if (!password) {
      setErrorMsg('Please enter your password.');
      return;
    }

    setLoading(true);

    try {
      if (isRegisterMode) {
        const res = await apiService.register(cleanUser, password);
        if (res.ok) {
          setSuccessMsg('Account created successfully! Signing in...');
          const loginRes = await apiService.login(cleanUser, password);
          if (loginRes.ok && loginRes.user) {
            onSuccess(loginRes.user);
          }
        } else {
          setErrorMsg(res.message || 'Registration failed.');
        }
      } else {
        const res = await apiService.login(cleanUser, password);
        if (res.ok && res.user) {
          onSuccess(res.user);
        } else {
          setErrorMsg('Unable to sign in. Please check your username and password.');
        }
      }
    } catch (err: any) {
      if (err.status === 401) {
        setErrorMsg('Invalid credentials. Please verify your username and password.');
      } else if (err.status === 0) {
        setErrorMsg('Aegis backend services are temporarily unreachable. Please ensure the API is running on port 8000.');
      } else {
        setErrorMsg(err.message || 'Authentication error. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      {/* Glass Card Container */}
      <div className="relative backdrop-blur-2xl bg-[rgba(15,10,32,0.85)] border border-violet-500/25 rounded-3xl p-8 sm:p-10 shadow-[0_25px_60px_rgba(8,3,20,0.85)] hover:border-violet-500/40 transition-all duration-300">
        {/* Glow ambient background highlight */}
        <div className="absolute -top-12 -right-12 w-48 h-48 bg-violet-600/20 rounded-full blur-[60px] pointer-events-none" />
        <div className="absolute -bottom-12 -left-12 w-48 h-48 bg-purple-600/15 rounded-full blur-[60px] pointer-events-none" />

        {/* Card Header */}
        <div className="mb-8 relative z-10 text-center sm:text-left">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            {isRegisterMode ? 'Create Account' : 'Welcome back'}
          </h2>
          <p className="text-sm text-violet-200/60 mt-1.5">
            {isRegisterMode
              ? 'Register to access Aegis Analytics AI intelligence platform.'
              : 'Sign in to continue to Aegis Analytics AI.'}
          </p>
        </div>

        {/* Alert Error Box */}
        {errorMsg && (
          <div className="mb-6 p-3.5 rounded-xl bg-rose-500/15 border border-rose-500/30 text-rose-200 text-xs sm:text-sm flex items-start gap-2.5 animate-fadeIn relative z-10">
            <svg className="w-4 h-4 text-rose-400 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{errorMsg}</span>
          </div>
        )}

        {/* Alert Success Box */}
        {successMsg && (
          <div className="mb-6 p-3.5 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-200 text-xs sm:text-sm flex items-start gap-2.5 animate-fadeIn relative z-10">
            <svg className="w-4 h-4 text-emerald-400 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
            </svg>
            <span>{successMsg}</span>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-5 relative z-10" noValidate>
          {/* Username/Email Input */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-violet-200/80 mb-2">
              Username or Email
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-violet-400/60">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <input
                type="text"
                value={username}
                onChange={e => setUsername(e.target.value)}
                placeholder="you@example.com or demo"
                disabled={loading}
                className="w-full pl-10 pr-4 py-3 bg-purple-950/40 border border-violet-500/25 rounded-xl text-white placeholder-violet-300/30 focus:outline-none focus:border-violet-500 focus:ring-2 focus:ring-violet-500/30 transition-all text-sm"
                required
              />
            </div>
          </div>

          {/* Password Input */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-violet-200/80 mb-2">
              Password
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-violet-400/60">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={e => setPassword(e.target.value)}
                placeholder="Enter password"
                disabled={loading}
                className="w-full pl-10 pr-10 py-3 bg-purple-950/40 border border-violet-500/25 rounded-xl text-white placeholder-violet-300/30 focus:outline-none focus:border-violet-500 focus:ring-2 focus:ring-violet-500/30 transition-all text-sm"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-violet-400/60 hover:text-violet-300 transition-colors"
                aria-label={showPassword ? 'Hide password' : 'Show password'}
              >
                {showPassword ? (
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858-5.908a10.03 10.03 0 013.682-.763c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21M3 3l18 18" />
                  </svg>
                ) : (
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                )}
              </button>
            </div>
          </div>

          {/* Options Row */}
          {!isRegisterMode && (
            <div className="flex items-center justify-between text-xs pt-1">
              <label className="flex items-center gap-2 text-violet-200/70 cursor-pointer select-none">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={e => setRememberMe(e.target.checked)}
                  className="rounded border-violet-500/40 bg-purple-950/60 text-violet-600 focus:ring-violet-500/40 w-3.5 h-3.5"
                />
                <span>Remember me</span>
              </label>
              <button
                type="button"
                onClick={() => setErrorMsg('For password reset, please contact system administrator.')}
                className="text-violet-400 hover:text-violet-300 transition-colors font-medium"
              >
                Forgot password?
              </button>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 px-6 rounded-xl bg-gradient-to-r from-violet-600 via-purple-600 to-indigo-600 hover:from-violet-500 hover:via-purple-500 hover:to-indigo-500 active:scale-[0.99] text-white font-bold text-sm tracking-wide shadow-[0_0_25px_rgba(124,58,237,0.4)] hover:shadow-[0_0_35px_rgba(124,58,237,0.6)] transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                <span>{isRegisterMode ? 'Registering...' : 'Signing in...'}</span>
              </>
            ) : (
              <span>{isRegisterMode ? 'Create Account' : 'Sign In'}</span>
            )}
          </button>
        </form>

        {/* Mode Toggle Link */}
        <div className="mt-6 text-center text-xs text-violet-300/70 relative z-10">
          <span>{isRegisterMode ? 'Already have an account?' : "Don't have an account?"}</span>{' '}
          <button
            type="button"
            onClick={() => {
              setIsRegisterMode(!isRegisterMode);
              setErrorMsg(null);
              setSuccessMsg(null);
            }}
            className="text-violet-300 hover:text-white font-semibold underline underline-offset-4 decoration-violet-500/50 hover:decoration-violet-300 transition-colors ml-1"
          >
            {isRegisterMode ? 'Sign in' : 'Create an account'}
          </button>
        </div>

        {/* Security & System Status Footer */}
        <div className="mt-8 pt-5 border-t border-violet-500/15 flex items-center justify-between text-[11px] text-violet-300/50 relative z-10">
          <span className="flex items-center gap-1.5">
            <svg className="w-3.5 h-3.5 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            Secure authentication
          </span>

          <span className="flex items-center gap-1.5">
            {systemOnline === true ? (
              <>
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                <span className="text-emerald-400/90 font-medium">Aegis Engine Online</span>
              </>
            ) : systemOnline === false ? (
              <>
                <span className="w-2 h-2 rounded-full bg-rose-500" />
                <span className="text-rose-400 font-medium">Backend Offline</span>
              </>
            ) : (
              <>
                <span className="w-2 h-2 rounded-full bg-amber-400 animate-ping" />
                <span>Checking Engine...</span>
              </>
            )}
          </span>
        </div>
      </div>
    </div>
  );
};
