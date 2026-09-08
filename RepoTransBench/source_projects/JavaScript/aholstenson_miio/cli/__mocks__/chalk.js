module.exports = {
  bgWhite: {
    black: (...args) => `[INFO] ${args.join(' ')}`
  },
  bgRed: {
    white: (...args) => `[ERROR] ${args.join(' ')}`
  },
  bgYellow: {
    black: (...args) => `[WARNING] ${args.join(' ')}`
  },
  bold: (...args) => `[BOLD] ${args.join(' ')}`
  ,
  green: text => `[GREEN] ${text}`,
  yellow: text => `[YELLOW] ${text}`,
};