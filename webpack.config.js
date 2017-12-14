var webpack = require('webpack')
var path = require('path')
var ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
    entry: {
        vendor: [
            path.resolve(__dirname, 'static/js/vendor.js'),
            path.resolve(__dirname, 'static/scss/vendor.scss')
        ],
        app: [
            path.resolve(__dirname, 'static/scss/main.scss')
        ]
    },
    output: {
        path: path.resolve(__dirname, 'static/dist'),
        filename: '[name].js'
    },

    module: {
        rules: [
            {
                test: /\.s[ac]ss$/,
                use: ExtractTextPlugin.extract({
                  fallback: "style-loader",
                  use: ['css-loader', 'sass-loader']
                })
            },
            {
              test: require.resolve('jquery'),
              use: [{
                  loader: 'expose-loader',
                  options: '$'
              }]
            }
        ]
    },
    plugins: [
      new webpack.ProvidePlugin({
         $: "jquery",
         jQuery: "jquery",
        'window.jQuery': 'jquery',
        Popper: ['popper.js', 'default'],
      }),
      new ExtractTextPlugin("[name].css"),
    ]
}