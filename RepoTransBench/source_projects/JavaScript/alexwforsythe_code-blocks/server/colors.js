// colors.js

const NAME_TO_HEX = {
  "black": "#000000",
  "white": "#ffffff",
  "red": "#ff0000",
  "lime": "#00ff00",
  "blue": "#0000ff",
};

function colorToHex(color) {
  if (typeof color !== 'string') return color;
  if (color[0] === '#' && color.length === 7) return color;
  if (color[0] === '#' && color.length === 4) {
    // expand 3-digit hex to 6-digit
    return '#' + color[1]+color[1] + color[2]+color[2] + color[3]+color[3];
  }
  if (NAME_TO_HEX[color.toLowerCase()]) {
    return NAME_TO_HEX[color.toLowerCase()];
  }
  return color;
}

module.exports = {
  colorToHex,
  NAME_TO_HEX
};