const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8080,  // 前端端口
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // Django 后端地址
        changeOrigin: true,  // 允许跨域
        ws: true,  // 支持 websocket
        pathRewrite: {
          '^/api': '/api'  // 路径重写，保持 api 前缀
        }
      }
    }
  }
})
