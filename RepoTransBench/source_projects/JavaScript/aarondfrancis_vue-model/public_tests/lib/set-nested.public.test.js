const assert = require('assert');
const setNested = require('../../src/lib/set-nested');

describe('setNested (public)', () => {
  it('sets a simple different key-value', () => {
    const obj = {};
    setNested(obj, 'alpha', 42);
    assert.deepStrictEqual(obj, { alpha: 42 });
  });

  it('sets a nested property with another path', () => {
    const obj = {};
    setNested(obj, 'x.y.z', 'test');
    assert.strictEqual(obj.x.y.z, 'test');
  });

  it('does not overwrite intermediate objects if already set, with different vals', () => {
    const obj = { n: { p: 11 } };
    setNested(obj, 'n.q', 22);
    assert.strictEqual(obj.n.p, 11);
    assert.strictEqual(obj.n.q, 22);
  });

  it('sets deep property with array index', () => {
    const obj = {};
    setNested(obj, 'arr.0.a', 'first');
    assert.strictEqual(obj.arr[0].a, 'first');
  });
});