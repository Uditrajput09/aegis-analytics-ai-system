/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        aegis: {
          bg: '#0A0914',
          'bg-subtle': '#0E0D1F',
          card: '#141226',
          'card-hover': '#1B1833',
          border: 'rgba(139, 92, 246, 0.15)',
          'border-bright': 'rgba(139, 92, 246, 0.35)',
          primary: '#7C3AED',
          'primary-bright': '#8B5CF6',
          secondary: '#6366F1',
          ai: '#A855F7',
          positive: '#10B981',
          warning: '#F59E0B',
          risk: '#EF4444',
          muted: '#94A3B8',
          text: '#F8FAFC',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'glow-purple': '0 0 25px -5px rgba(124, 58, 237, 0.4)',
        'glow-sm': '0 0 15px -3px rgba(139, 92, 246, 0.3)',
        'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
      },
      backgroundImage: {
        'purple-gradient': 'linear-gradient(135deg, #7C3AED 0%, #4F46E5 100%)',
        'card-gradient': 'linear-gradient(180deg, rgba(20, 18, 38, 0.8) 0%, rgba(14, 13, 31, 0.9) 100%)',
        'glow-gradient': 'radial-gradient(circle at top right, rgba(124, 58, 237, 0.15), transparent 70%)',
      }
    },
  },
  plugins: [],
}
