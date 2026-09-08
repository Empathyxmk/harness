const assert = require('assert');
const Errors = require('../src/Errors');

describe('Errors (public)', () => {
  it('can construct empty errors', () => {
    const e = new Errors();
    assert.deepStrictEqual(e.all(), {});
  });

  it('set/get/has/clear for other paths', () => {
    const e = new Errors();
    e.set('alpha', 'beta');
    assert.strictEqual(e.has('alpha'), true);
    assert.strictEqual(e.get('alpha'), 'beta');
    assert.strictEqual(e.has('gamma'), false);
    e.clear('alpha');
    assert.strictEqual(e.has('alpha'), false);
  });

  it('push and get first for other key', () => {
    const e = new Errors();
    e.push('delta', 'errX');
    e.push('delta', 'errY');
    assert.deepStrictEqual(e.get('delta'), ['errX', 'errY']);
    assert.strictEqual(e.first('delta'), 'errX');
    assert.strictEqual(e.first('epsilon'), undefined);
  });

  it('merge with other errors', () => {
    const e1 = new Errors();
    e1.push('theta', 'm');
    const e2 = new Errors();
    e2.push('theta', 'n');
    e1.merge(e2);
    assert.deepStrictEqual(e1.get('theta'), ['m', 'n']);
  });

  it('stringifies as json, other data', () => {
    const e = new Errors();
    e.push('omega', 'psi');
    assert.ok(e.toString().includes('omega'), 'Should stringify field name');
    assert.ok(e.toString().includes('psi'), 'Should stringify error');
  });
});