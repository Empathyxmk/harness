// Switched to correct Babel configuration. Remove all reference to 'babel-preset-es2015'.
module.exports = {
  presets: [
    ["@babel/preset-env", { targets: { node: "current" } }]
  ]
};