import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true
  },
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        menu: resolve(__dirname, 'menu1.html'),
        menu2: resolve(__dirname, 'menu2.html'),
        menu3: resolve(__dirname, 'menu3.html'),
        menu4: resolve(__dirname, 'menu4.html'),
        menu5: resolve(__dirname, 'menu5.html'),
        concessions: resolve(__dirname, 'concessions.html'),
        confirmation: resolve(__dirname, 'confirmation.html')
      }
    }
  }
})
