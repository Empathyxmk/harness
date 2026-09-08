const assert = require('assert');

describe('fuge.js basic', function () {
  it('can load fuge.js without error', function () {
    assert.doesNotThrow(() => require('../fuge.js'));
  });

  it('main exported value is a function', function () {
    const mod = require('../fuge.js');
    assert.strictEqual(typeof mod, 'function');
  });

  it('calling main returns object or throws usage error', function () {
    const mod = require('../fuge.js');
    let threw = false;
    try {
      // Pass minimal possible config, e.g. an empty object:
      const obj = mod({});
      // Should return an object, but could fail if strict args required
      assert(obj && typeof obj === 'object');
    } catch (e) {
      threw = true;
    }
    assert.strictEqual(threw, false, 'fuge() call threw unexpectedly');
  });
});