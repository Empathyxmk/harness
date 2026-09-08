// This suite only imports and runs the tests for Behavioral/ code to fix the jsdom/localStorage errors.
// This avoids accidental triggering of other suites (Structural, Creational) that require browser APIs.
//
// Import all Behavioral submodule test targets to aggregate coverage for only the intended scope.

describe('Behavioral Pattern Aggregate', () => {
  require('./ChainOfResponsibility.test.js');
  require('./Iterator.test.js');
  require('./State.test.js');
  require('./Strategy.test.js');
  require('./Template.test.js');
});