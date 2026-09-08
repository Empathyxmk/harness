// bar.js - minimally export a function/object to allow coverage

module.exports = {
  add: function (x = 0, y = 0) {
    if (isNaN(x) || isNaN(y)) {
      throw new Error('Invalid number');
    }
    return x + y;
  }
};