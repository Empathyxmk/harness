const AuthenticationError = require('../lib/errors/authenticationerror');
const assert = require('assert');

describe('AuthenticationError (public)', function() {
  it('should set message and status with different message', function() {
    const err = new AuthenticationError('public error');
    assert.strictEqual(err.name, 'AuthenticationError');
    assert.strictEqual(err.message, 'public error');
    assert.strictEqual(err.status, 401);
    assert.ok(err.stack);
  });

  it('should allow custom status (different value)', function() {
    const err = new AuthenticationError('forbidden', 418);
    assert.strictEqual(err.status, 418);
  });

  it('should inherit from Error (different instance)', function() {
    const err = new AuthenticationError('bar');
    assert.ok(err instanceof Error);
  });
});