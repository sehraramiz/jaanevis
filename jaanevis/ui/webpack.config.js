const path = require('path');
const Dotenv = require('dotenv-webpack')

module.exports = (env) => {
  return {
    mode: 'development',
    entry: './src/app.js',
    output: {
      path: path.resolve(__dirname, 'dist'),
      filename: 'main.js',
    },
    module: {
      rules: [
        {
          test: /\.css$/i,
          use: ['style-loader', 'css-loader'],
        },
      ],
    },
    plugins: [
      new Dotenv({
        path: "./.env" + (env.target ? `.${env.target}`: ".dev")
      })
    ]
  };
}
