// Fixed: Ensure correct instantiation and methods for Errors class
const assert = require('assert');
const Errors = require('./Errors');

describe('Errors', () => {
  it('can construct empty', () => {
    const e = new Errors();
    assert.deepStrictEqual(e.all(), {});
  });

  it('set/get/has/clear to cover paths', () => {
    const e = new Errors();
    e.set('foo', 'bar');
    assert.strictEqual(e.has('foo'), true);
    assert.strictEqual(e.get('foo'), 'bar');
    assert.strictEqual(e.has('baz'), false);
    e.clear('foo');
    assert.strictEqual(e.has('foo'), false);
  });

  it('push and get first', () => {
    const e = new Errors();
    e.push('foo', 'err1');
    e.push('foo', 'err2');
    assert.deepStrictEqual(e.get('foo'), ['err1', 'err2']);
    assert.strictEqual(e.first('foo'), 'err1');
    assert.strictEqual(e.first('bar'), undefined);
  });

  it('merge', () => {
    const e1 = new Errors();
    e1.push('foo', 'a');
    const e2 = new Errors();
    e2.push('foo', 'b');
    e1.merge(e2);
    assert.deepStrictEqual(e1.get('foo'), ['a', 'b']);
  });

  it('stringifies as json', () => {
    const e = new Errors();
    e.push('foo', 'bar');
    assert.ok(e.toString().includes('foo'), 'Should stringify field name');
    assert.ok(e.toString().includes('bar'), 'Should stringify error');
  });
});