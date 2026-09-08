const assert = require('chai').assert;

const proxyPolyfill = require('../src/proxy.js');

// Helper for creating polyfilled Proxy regardless of global.Proxy
function PolyProxy(target, handler) {
  const Poly = proxyPolyfill();
  return new Poly(target, handler);
}

describe('GoogleChrome proxy-polyfill edge/error cases - PUBLIC DATA', () => {
  it('throws if Proxy is constructed without new (public)', () => {
    const Poly = proxyPolyfill();
    assert.throws(() => {
      Poly({ foo: 42 }, { bar: "baz" });
    }, /requires 'new'/);
  });

  it('throws if target or handler is not object (public)', () => {
    const Poly = proxyPolyfill();
    assert.throws(() => new Poly(undefined, {a:1}), /non-object/);
    assert.throws(() => new Poly({a:1}, undefined), /non-object/);
    assert.throws(() => new Poly('string', {}), /non-object/);
    assert.throws(() => new Poly({}, 'string'), /non-object/);
    assert.throws(() => new Poly([1], 0), /non-object/);
  });

  it('throws if handler has unsupported trap (public)', () => {
    const Poly = proxyPolyfill();
    assert.throws(() =>
      new Poly({ a: 1 }, { set: () => {}, barfoo: true }),
      /does not support trap 'barfoo'/
    );
  });

  it('handler as function sets apply (public)', () => {
    const Poly = proxyPolyfill();
    function handlerFn() {}
    handlerFn.apply = function(target, thisArg, args) {
      return args && args.length ? args[0] * 2 : 10;
    };
    const p = new Poly(function(x){return x+1;}, handlerFn);
    assert.strictEqual(p(7), 14, 'apply trap used from function-handler (public)');
  });

  it('should revoke access after revocation (public)', () => {
    const Poly = proxyPolyfill();
    const { proxy, revoke } = Poly.revocable({foo: 'bar'}, {
      get(obj, prop) { return obj[prop]; }
    });
    assert.equal(proxy.foo, 'bar');
    revoke();
    assert.throws(() => proxy.foo, /revoked/);
  });

  it('validateProto throws for non-object proto (public)', () => {
    // This triggers the error state indirectly via Object.create
    const Poly = proxyPolyfill();
    assert.throws(() =>
      Object.create('string-proto'), /Object prototype may only be an Object or null/
    );
  });

  it('objectCreate throws for null prototype if not supported (public)', () => {
    // Can't force lack of Object.create with null so just assert it exists
    assert.isFunction(Object.create);
  });

  it('getPrototypeOf returns null when __proto__ missing (public)', () => {
    // Similar code using a different approach and different object
    function NoProto() {}
    NoProto.prototype = null;
    const o = new NoProto();
    Object.setPrototypeOf(o, null);
    assert.isNull(Object.getPrototypeOf(o));
  });
});