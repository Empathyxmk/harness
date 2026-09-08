// pie.js - minimally export a function/object to allow coverage

module.exports = {
  slices: function (n) {
    if (typeof n !== 'number' || n < 1) return [];
    return Array.from({ length: n }, (_, i) => i + 1);
  }
};