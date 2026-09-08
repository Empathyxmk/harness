const passport = require('../lib/index');
const assert = require('assert');

describe('passport export', function() {
  it('should export a singleton instance', function() {
    const p1 = require('../lib/index');
    const p2 = require('../lib/index');
    assert.strictEqual(p1, p2);
    assert.strictEqual(typeof p1.use, 'function');
  });

  it('should export Authenticator and Passport as constructors', function() {
    assert.ok(typeof passport.Authenticator === 'function');
    assert.ok(typeof passport.Passport === 'function');
    assert.ok(passport.Authenticator === passport.Passport);
  });

  it('should export strategies.SessionStrategy', function() {
    assert.ok(passport.strategies.SessionStrategy);
  });

  it('should export Strategy', function() {
    assert.ok(passport.Strategy);
  });
});