const assert = require('assert');
const setNested = require('./set-nested');

describe('setNested', () => {
  it('sets value deeply in object', () => {
    const obj = {};
    setNested(obj, 'a.b.c', 42);
    assert.strictEqual(obj.a.b.c, 42);
  });
  it('sets value with custom separator', () => {
    const obj = {};
    setNested(obj, 'a:b:c', 10, ':');
    assert.strictEqual(obj.a.b.c, 10);
  });
  it('overwrites existing sub-objects', () => {
    const obj = {a: {b: 5}};
    setNested(obj, 'a.b.c', 99);
    assert.deepStrictEqual(obj.a.b, {c: 99}, 'Should overwrite inner b');
  });
});