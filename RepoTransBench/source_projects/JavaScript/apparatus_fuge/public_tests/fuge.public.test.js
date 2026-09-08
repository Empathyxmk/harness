const assert = require('assert');
const fuge = require('../fuge');

describe('fuge.js public API', function () {
  it('has at least one exported key', function () {
    const keys = Object.keys(fuge);
    assert(keys.length >= 1);
  });

  it('should NOT throw when called with no arguments (public)', function () {
    // Try calling with no arguments, if exported function exists
    for (const k in fuge) {
      if (typeof fuge[k] === 'function') {
        assert.doesNotThrow(() => { fuge[k](); });
        break;
      }
    }
  });
});