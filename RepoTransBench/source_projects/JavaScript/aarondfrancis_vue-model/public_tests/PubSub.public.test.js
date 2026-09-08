const assert = require('assert');
const PubSub = require('../src/PubSub');

describe('PubSub (public)', () => {
  it('can subscribe and publish with different value', () => {
    const ps = new PubSub();
    let val = null;
    ps.subscribe('b', v => { val = v; });
    ps.publish('b', 456);
    assert.strictEqual(val, 456);
  });

  it('multiple subscribers, other values', () => {
    const ps = new PubSub();
    let v1 = 0, v2 = 0;
    ps.subscribe('y', v => { v1 = v; });
    ps.subscribe('y', v => { v2 = v + 3; });
    ps.publish('y', 7);
    assert.strictEqual(v1, 7);
    assert.strictEqual(v2, 10);
  });

  it('unsubscribe works with another key/value', () => {
    const ps = new PubSub();
    let calls = 0;
    function increment(x) { calls -= x; }
    ps.subscribe('w', increment);
    ps.unsubscribe('w', increment);
    ps.publish('w', 9); // Should not call increment
    assert.strictEqual(calls, 0);
  });

  it('publishing to no subscribers with different key/value', () => {
    const ps = new PubSub();
    // Should not throw
    ps.publish('nobody', 999);
  });
});