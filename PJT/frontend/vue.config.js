module.exports = {
  publicPath: "/",
  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:8000/",
      },
    },
  },
  transpileDependencies: ["vuetify"],
};
