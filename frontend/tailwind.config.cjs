module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Apple Design System Colors
        primary: '#0071e3',
        primaryHover: '#0077ed',
        primaryActive: '#0066cc',
        secondary: '#86868b',
        accent: '#34c759',
        warning: '#ff9500',
        error: '#ff3b30',
        
        // Background Colors
        background: '#f5f5f7',
        backgroundSecondary: '#ffffff',
        backgroundTertiary: '#f2f2f7',
        
        // Text Colors
        text: '#1d1d1f',
        textSecondary: '#86868b',
        textTertiary: '#c7c7cc',
        
        // Border Colors
        border: '#d2d2d7',
        borderSecondary: '#e5e5ea',
        borderTertiary: '#f2f2f7',
        
        // Card Colors
        card: '#ffffff',
        cardHover: '#fafafa',
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', 'SF Pro Display', 'Segoe UI', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        'apple': '18px',
        'apple-sm': '12px',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'fade-in-slow': 'fadeIn 0.8s ease-in-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'slide-up-slow': 'slideUp 0.8s ease-out',
        'bounce-slow': 'bounce 2s infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
      boxShadow: {
        'apple': '0 2px 10px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1)',
        'apple-hover': '0 4px 20px rgba(0, 0, 0, 0.1), 0 2px 6px rgba(0, 0, 0, 0.15)',
        'apple-lift': '0 8px 30px rgba(0, 0, 0, 0.12), 0 2px 7px rgba(0, 0, 0, 0.1)',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}