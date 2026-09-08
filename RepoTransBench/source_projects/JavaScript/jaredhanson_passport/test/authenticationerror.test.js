const AuthenticationError = require('../lib/errors/authenticationerror');
const assert = require('assert');

describe('AuthenticationError', function() {
  it('should set message and status', function() {
    const err = new AuthenticationError('failmessage');
    assert.strictEqual(err.name, 'AuthenticationError');
    assert.strictEqual(err.message, 'failmessage');
    assert.strictEqual(err.status, 401);
    assert.ok(err.stack);
  });

  it('should allow custom status', function() {
    const err = new AuthenticationError('err', 403);
    assert.strictEqual(err.status, 403);
  });

  it('should inherit from Error', function() {
    const err = new AuthenticationError('foo');
    assert.ok(err instanceof Error);
  });
});