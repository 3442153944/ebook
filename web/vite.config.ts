import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import VueDevTools from 'vite-plugin-vue-devtools'
import VueSetupExtension from 'vite-plugin-vue-setup-extend'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(),
    VueDevTools(),
    VueSetupExtension()
  ],
  resolve: {
    alias: {
      '@assets': path.resolve(process.cwd(), 'src/assets'),  // 将 @assets 映射到 src/assets
      '@': path.resolve(process.cwd(), 'src')  // 可选：同时配置 @ 别名指向 src 根目录
    }
  }
})
