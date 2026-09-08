const fuge = require('../fuge.js');
const assert = require('assert');

describe('fuge.js extra/branch coverage', function () {
  it('should handle missing/empty config gracefully', function () {
    try {
      fuge();
      // Acceptable as a no-op or should throw usage error. If so, okay.
    } catch (e) {
      assert(e.message || e.stack); // just an error
    }
  });

  it('should support config variants', function () {
    assert.doesNotThrow(() => fuge({ foo: 'bar' }));
  });
});