import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: './', // Base path relativo per GitHub Pages (risolve problemi di path assoluti)
  build: {
    // La directory di output deve corrispondere a quella usata da Flask
    outDir: 'build',
    emptyOutDir: true,
  },
})
