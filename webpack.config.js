const fs = require('fs');
const path = require('path');

const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const WebpackOnBuildPlugin = require('on-build-webpack');

const entryPath = path.resolve(__dirname, 'wagtail_advanced_form_builder/static_src/wagtail_advanced_form_builder');
const outputPath = path.resolve(__dirname, 'wagtail_advanced_form_builder/static/wagtail_advanced_form_builder');

const configureBabelLoader = () => {
    return {
        test: /\.js$/,
        exclude: /node_modules/,
        use: [
            'cache-loader',
            {
                loader: 'babel-loader',
            },
        ],
    };
};

module.exports = {
  mode: 'production',
  entry: {
    'style': path.join(entryPath, 'scss/main.scss'),
    'admin': path.join(entryPath, 'js/admin.js'),
    'formbuilder': path.join(entryPath, 'js/formbuilder.js'),
  },
  output: {
    path: outputPath,
    publicPath: '/wagtail_advanced_form_builder/static/wagtail_advanced_form_builder/',
    filename: `js/[name].js`
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader'
        ]
      },
      configureBabelLoader(),
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: `css/[name].css`
    }),
    new WebpackOnBuildPlugin(function () {
    })
  ]
};
