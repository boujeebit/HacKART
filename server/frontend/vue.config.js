module.exports = {
  lintOnSave: false,
  runtimeCompiler: true,
  devServer: {
    proxy: {
      "^/api/": {
        target: "http://localhost:8000",
        changeOrigin: true
      }
    }
  }
}