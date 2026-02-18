import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import history from 'connect-history-api-fallback'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8080',
        changeOrigin: true,
        timeout: 600000, // 增加超时时间到10分钟，匹配后端LLM_TIMEOUT设置
        secure: false,
        ws: true,
        // 增加重连机制
        onProxyReq: (proxyReq, req, res) => {
          console.log('Proxying request:', req.method, req.url)
        },
        onProxyRes: (proxyRes, req, res) => {
          console.log('Proxy response:', proxyRes.statusCode, req.url)
        },
        onError: (err, req, res) => {
          console.error('Proxy error:', err.message, req.url)
          // 返回504网关超时，而不是直接关闭连接
          res.writeHead(504, { 'Content-Type': 'application/json' })
          res.end(JSON.stringify({ error: 'Gateway Timeout', message: '请求处理超时，请稍后重试' }))
        }
      },
    },
    middleware: [history()],
  },
  preview: {
    port: 4173,
    host: '0.0.0.0',
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8080',
        changeOrigin: true,
        timeout: 600000, // 增加超时时间到10分钟，匹配后端LLM_TIMEOUT设置
        secure: false,
        ws: true,
        // 增加重连机制
        onProxyReq: (proxyReq, req, res) => {
          console.log('Proxying request:', req.method, req.url)
        },
        onProxyRes: (proxyRes, req, res) => {
          console.log('Proxy response:', proxyRes.statusCode, req.url)
        },
        onError: (err, req, res) => {
          console.error('Proxy error:', err.message, req.url)
          // 返回504网关超时，而不是直接关闭连接
          res.writeHead(504, { 'Content-Type': 'application/json' })
          res.end(JSON.stringify({ error: 'Gateway Timeout', message: '请求处理超时，请稍后重试' }))
        }
      },
    },
    // 简化middleware配置，确保API代理正常工作
    middleware: [],
  },
})