var _ = require('lodash');
var path = require('path');
var webpack = require('webpack');
var CommonsChunkPlugin = webpack.optimize.CommonsChunkPlugin;
var scripts = require('./scripts');

var aliases = _.mapValues(scripts.aliases, function(scriptPath) {
  return path.resolve(__dirname + scriptPath)
});

module.exports = {
  resolve : {
    alias: aliases
  },
  entry: {
    index: './index.js',
    vendor: [
      'three',
      'jquery'  ,
      'flot/jquery.flot',
      'flot/jquery.flot.time'
    ]
  },
  output: {
    path: __dirname,
    filename: '[name].bundle.js',
  },
  plugins: [
    new CommonsChunkPlugin("vendor", "vendor.bundle.js"),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery"
    })
  ]
}
