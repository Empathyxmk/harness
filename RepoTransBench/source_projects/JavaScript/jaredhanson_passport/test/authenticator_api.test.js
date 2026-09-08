const Authenticator = require('../lib/authenticator');
const assert = require('assert');

describe('Authenticator', function() {
  it('should be constructable', function() {
    const a = new Authenticator();
    assert.ok(a instanceof Authenticator);
    assert.strictEqual(a._key, 'passport');
  });

  it('should register a strategy', function() {
    const a = new Authenticator();
    let s = { name: 'foo' };
    a.use(s);
    assert.strictEqual(a._strategies['foo'], s);
  });

  it('should register a strategy with explicit name', function() {
    const a = new Authenticator();
    let s = {};
    a.use('bar', s);
    assert.strictEqual(a._strategies['bar'], s);
  });

  it('should throw if no name on strategy', function() {
    const a = new Authenticator();
    assert.throws(() => a.use({}), /Authentication strategies must have a name/);
  });

  it('should unuse a strategy', function() {
    const a = new Authenticator();
    let s = { name: 'zap' };
    a.use(s);
    a.unuse('zap');
    assert.strictEqual(a._strategies['zap'], undefined);
  });

  it('should call framework()', function() {
    const a = new Authenticator();
    let obj = {};
    assert.strictEqual(a.framework(obj), a);
    assert.strictEqual(a._framework, obj);
  });
});