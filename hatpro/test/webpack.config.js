var path = require('path');
var webpack = require('webpack');
var CommonsChunkPlugin = webpack.optimize.CommonsChunkPlugin;

module.exports = {

  entry: {
    index: './index.js',
    vendor: ['three', 'jquery']
  },

  output: {
    path: __dirname,
    filename: '[name].bundle.js'
  },

  plugins: [
    new CommonsChunkPlugin("vendor", "vendor.bundle.js")
  ]
}
