// Public test for main index.js exports using different data

const passport = require('../lib');
const assert = require('assert');

describe('passport module (public)', function () {
  it('should export initialize and authenticate as functions', function () {
    assert.strictEqual(typeof passport.initialize, 'function');
    assert.strictEqual(typeof passport.authenticate, 'function');
  });

  it('should export Authenticator with a new instance', function () {
    assert.ok(passport.Authenticator);
    const instance = new passport.Authenticator();
    assert.ok(instance);
    instance.use({ name: 'public-test-foo' });
    assert.ok(instance._strategies['public-test-foo']);
  });
});