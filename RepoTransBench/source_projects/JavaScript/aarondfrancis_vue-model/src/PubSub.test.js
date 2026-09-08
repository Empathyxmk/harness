const assert = require('assert');
const PubSub = require('./PubSub');

describe('PubSub', () => {
  it('can subscribe and publish', () => {
    const ps = new PubSub();
    let val = null;
    ps.subscribe('a', v => { val = v; });
    ps.publish('a', 123);
    assert.strictEqual(val, 123);
  });

  it('multiple subscribers work', () => {
    const ps = new PubSub();
    let v1 = 0, v2 = 0;
    ps.subscribe('z', v => { v1 = v; });
    ps.subscribe('z', v => { v2 = v * 2; });
    ps.publish('z', 4);
    assert.strictEqual(v1, 4);
    assert.strictEqual(v2, 8);
  });

  it('unsubscribe works', () => {
    const ps = new PubSub();
    let called = 0;
    function fn(x) { called += x; }
    ps.subscribe('x', fn);
    ps.unsubscribe('x', fn);
    ps.publish('x', 5); // Should not call fn
    assert.strictEqual(called, 0);
  });

  it('publishing to no subscribers does nothing', () => {
    const ps = new PubSub();
    // Should not throw
    ps.publish('never', 77);
  });
});