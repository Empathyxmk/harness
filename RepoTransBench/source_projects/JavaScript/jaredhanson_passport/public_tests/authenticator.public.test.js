// Public tests for lib/authenticator.js using different test data than existing tests

const Authenticator = require('../lib/authenticator');
const assert = require('assert');

describe('Authenticator (public)', function () {
  it('should construct with a unique name', function () {
    const authenticator = new Authenticator();
    assert.ok(authenticator);
  });

  it('should register a new strategy with a different name', function () {
    const authenticator = new Authenticator();
    const dummyStrategy = { name: 'mock-strategy-xyz' };
    authenticator.use(dummyStrategy);
    assert.ok(authenticator._strategies['mock-strategy-xyz']);
  });

  it('should throw error for unknown strategy', function () {
    const authenticator = new Authenticator();
    assert.throws(() => authenticator.authenticate('nonexistent-strategy-789'), /Unknown authentication strategy/);
  });
});