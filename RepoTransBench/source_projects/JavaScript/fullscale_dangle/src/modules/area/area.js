// area.js - minimally export a function/object to allow coverage

module.exports = {
  exampleMethodArea: function (a = 1, b = 1) {
    // Simple branch to hit coverage targets
    if (a > b) {
      return 'a';
    } else if (a < b) {
      return 'b';
    } else {
      return 'equal';
    }
  }
};