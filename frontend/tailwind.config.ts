import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'card-dark': '#1a1a2e',
        'card-darker': '#0f0f23',
        'grade-s': '#ffd700',
        'grade-a': '#a855f7',
        'grade-b': '#3b82f6',
        'grade-c': '#22c55e',
        'grade-d': '#6b7280',
      },
      boxShadow: {
        'glow-gold': '0 0 20px rgba(255, 215, 0, 0.3)',
        'glow-purple': '0 0 20px rgba(168, 85, 247, 0.3)',
        'glow-blue': '0 0 20px rgba(59, 130, 246, 0.3)',
        'glow-green': '0 0 20px rgba(34, 197, 94, 0.3)',
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
