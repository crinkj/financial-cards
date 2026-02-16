import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'navy': '#0F172A',
        'navy-light': '#1E293B',
        'navy-lighter': '#334155',
        'card-dark': '#1E293B',
        'card-darker': '#0F172A',
        'grade-s': '#ffd700',
        'grade-a': '#a855f7',
        'grade-b': '#3b82f6',
        'grade-c': '#10b981',
        'grade-d': '#6b7280',
        'accent': '#10B981',
      },
      boxShadow: {
        'glow-gold': '0 0 16px rgba(255, 215, 0, 0.2)',
        'glow-purple': '0 0 16px rgba(168, 85, 247, 0.2)',
        'glow-blue': '0 0 16px rgba(59, 130, 246, 0.2)',
        'glow-green': '0 0 16px rgba(16, 185, 129, 0.2)',
        'card': '0 1px 3px rgba(0, 0, 0, 0.3), 0 1px 2px rgba(0, 0, 0, 0.2)',
        'card-hover': '0 4px 12px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(16, 185, 129, 0.1)',
      },
      animation: {
        'flip': 'flip 0.6s ease-in-out',
      },
      keyframes: {
        flip: {
          '0%': { transform: 'rotateY(0deg)' },
          '100%': { transform: 'rotateY(180deg)' },
        },
      },
    },
  },
  plugins: [],
}
export default config
