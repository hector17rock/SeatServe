import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'
import { fileURLToPath } from 'url'
import fs from 'fs'

const __dirname = fileURLToPath(new URL('.', import.meta.url))

// Dynamically find all HTML files in root
const getHtmlFiles = () => {
  const input = { main: resolve(__dirname, 'index.html') }
  const files = fs.readdirSync(__dirname)
  files.forEach(file => {
    if (file.endsWith('.html') && file !== 'index.html') {
      const name = file.replace('.html', '')
      input[name] = resolve(__dirname, file)
    }
  })
  return input
}

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  },
  build: {
    rollupOptions: {
      input: getHtmlFiles(),
      output: {
        entryFileNames: '[name]-[hash].js',
        chunkFileNames: '[name]-[hash].js',
        assetFileNames: '[name]-[hash][extname]'
      }
    }
  }
})
