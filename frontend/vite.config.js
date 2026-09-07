import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  // Configuração necessária para rodar dentro do Docker: por padrão o
  // Vite só escuta em "localhost" dentro do container, o que o deixa
  // inacessível de fora. "0.0.0.0" expõe o servidor para qualquer
  // interface de rede, permitindo que o Docker Compose mapeie a porta
  // para a máquina host.
  server: {
    host: '0.0.0.0',
    port: 5173,
  },
})
