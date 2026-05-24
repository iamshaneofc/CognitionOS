/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: 'class', // Support toggleable system dark modes
  theme: {
    extend: {
      colors: {
        // High-end dark theme foundation
        bg: {
          darkest: '#090a0f',
          darker: '#0f111a',
          dark: '#161925',
          card: '#1e2235',
        },
        // Harmonious semantic palette representing cognitive states
        state: {
          overload: '#ff4d6d',      // Soft vibrant crimson for stress/overload
          drift: '#ff9f1c',         // Amber for behavioral drift indicator
          optimal: '#2ec4b6',       // Emerald/teal for emotional balance/focus
          recovery: '#4cc9f0',      // Cyan for sleep/recovery phases
          cognitive: '#7209b7',     // Purple for deep cognitive activity
        },
        accent: {
          neon: '#8a2be2',
          glow: 'rgba(138, 43, 226, 0.15)',
        }
      },
      fontFamily: {
        sans: ['Inter', 'Outfit', 'sans-serif'],
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
        'glass-highlight': 'inset 0 1px 0 0 rgba(255, 255, 255, 0.05)',
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow-spin': 'spin 8s linear infinite',
      }
    },
  },
  plugins: [],
}
