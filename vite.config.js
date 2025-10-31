import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/G-Site/', // Base path assoluto per GitHub Pages (nome del repository)
  build: {
    // La directory di output deve corrispondere a quella usata da Flask
    outDir: 'build',
    emptyOutDir: true,
  },
})
