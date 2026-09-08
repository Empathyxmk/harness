// Bootstrap file for Mocha: makes chai globally available and loads any plugins.
// This ensures that `expect` and `chai.passport` are present in all tests.

const chai = require('chai');
global.expect = chai.expect;

// Only load passport-chai if available and not already loaded
try {
  require.resolve('chai-passport-strategy');
  chai.use(require('chai-passport-strategy'));
  global.chai = chai;
} catch (e) {
  // chai-passport-strategy not installed; tests depending on it may fail
}