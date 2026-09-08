const assert = require('assert');

describe('nconf', function () {
  it('should load configuration', function () {
    const nconf = require('../../src/nconf.js');
    assert.ok(nconf);
    assert.ok(typeof nconf.get === 'function' || typeof nconf.argv === 'function');
  });
});