// column.js - minimally export a function/object to allow coverage

module.exports = {
  stringToUpper: function (s) {
    if (!s) return '';
    return s.toUpperCase();
  }
};