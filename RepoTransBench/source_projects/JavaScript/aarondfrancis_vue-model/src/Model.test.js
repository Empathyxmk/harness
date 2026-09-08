const assert = require('assert');
const Model = require('./Model');

describe('Model', () => {
  it('can be instantiated', () => {
    const m = new Model({foo: 1});
    assert.ok(m);
    assert.strictEqual(m.foo, 1);
  });

  it('prototype has expected methods', () => {
    // Just check for methods
    const fns = [
      'save', 'fill', 'sync', 'clear', 'clone', 'toObject', 'reset',
      'merge', 'update', 'fresh', 'exists', 'flush', 'setKey', 'getKey'
    ];
    fns.forEach(fn => {
      assert.ok(typeof Model.prototype[fn] === 'function', fn + ' missing');
    });
  });

  it('assigns attributes and can reset', () => {
    const m = new Model({foo: 'bar'});
    m.foo = 'baz';
    m.reset();
    assert.strictEqual(m.foo, 'bar');
  });
});