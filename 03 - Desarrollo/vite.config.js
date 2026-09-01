import { defineConfig } from 'vite'
import react, { reactCompilerPreset } from '@vitejs/plugin-react'
import babel from '@rolldown/plugin-babel'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    babel({ presets: [reactCompilerPreset()] }),
    tailwindcss(),
  ],
  resolve: {
    dedupe: ['react', 'react-dom', 'react-router-dom', 'recharts'],
  },
  optimizeDeps: {
    include: [
      'react',
      'react/jsx-dev-runtime',
      'react/compiler-runtime',
      'react-dom',
      'react-dom/client',
      'react-router-dom',
      'recharts',
    ],
  },
  server: {
    host: true,
    port: 5173,
    strictPort: true,
  },
})
