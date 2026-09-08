const assert = require('assert');
const Model = require('../src/Model');

describe('Model (public)', () => {
  it('can be instantiated with new field', () => {
    const m = new Model({bar: 2});
    assert.ok(m);
    assert.strictEqual(m.bar, 2);
  });

  it('prototype retains required methods', () => {
    // Just check for methods (same as before)
    const fns = [
      'save', 'fill', 'sync', 'clear', 'clone', 'toObject', 'reset',
      'merge', 'update', 'fresh', 'exists', 'flush', 'setKey', 'getKey'
    ];
    fns.forEach(fn => {
      assert.ok(typeof Model.prototype[fn] === 'function', fn + ' missing');
    });
  });

  it('assigns other attributes and can reset', () => {
    const m = new Model({bar: 'baz'});
    m.bar = 'qux';
    m.reset();
    assert.strictEqual(m.bar, 'baz');
  });
});