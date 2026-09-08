// dangle.module.js
// Minimal definition for coverage and testability (works outside browser context)

// In browser/AngularJS, this defines angular.module("dangle", []);
// For Node.js/CommonJS, we just export a function/object for code coverage.

module.exports = function dangleModule() {
  // No-op, placeholder to make module export exist for coverage
  return "dangle";
};