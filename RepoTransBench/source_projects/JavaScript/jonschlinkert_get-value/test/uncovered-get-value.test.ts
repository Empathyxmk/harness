import assert from 'assert';
import getValue from '../index';

// Test for code paths not covered by existing tests

describe('get-value uncovered code', () => {
  it('should handle path as array with numbers and non-strings', () => {
    const obj = { foo: { 1: { bar: 'baz' } } };
    assert.strictEqual(getValue(obj, ['foo', 1, 'bar']), 'baz');
  });

  it('should join segments with join() option returning only first element', () => {
    // force option.join to a function that returns only a single segment
    function joinOnlyFirst(segs: string[]) {
      return segs[0];
    }
    const obj = { foo: { bar: 'baz' } };
    const options = { join: joinOnlyFirst };
    // Still returns correct because join is used only for escaped segments case
    assert.strictEqual(getValue(obj, ['foo', 'bar'], options), 'baz');
  });

  it('should parse options separator when it is not a string (test joinChar fallback)', () => {
    const obj = { a: { b: 'c' } };
    const weirdOptions = { separator: /[.]/ }; // separator as regex
    assert.strictEqual(getValue(obj, 'a.b', weirdOptions), 'c');
  });

  it('should handle object key being undefined, returning options.default', () => {
    const obj: any = {};
    assert.strictEqual(getValue(obj, undefined as any, { default: 'zz' }), 'zz');
  });

  it('should return the value from root array index', () => {
    const arr = [1, 2, 3];
    assert.strictEqual(getValue(arr, 0), 1);
  });

  it('should return target[path] if found when path is array', () => {
    const obj = { foo: { bar: 'baz' }, 'foo,bar': 'zip' };
    // This triggers direct property lookup, as path is "foo,bar"
    assert.strictEqual(getValue(obj, ['foo,bar']), 'zip');
  });

  it('should handle property escaping with multiple segments and join function', () => {
    const obj = { 'a.b.c': { x: 1 } };
    const options = {
      join: (segs: string[]) => segs.join('*'),
      separator: '.',
      joinChar: '*'
    };
    assert.strictEqual(getValue(obj, 'a\\.b\\.c.x', options), 1);
  });

  it('should not treat a function as a valid object if options.isValid filters it out', () => {
    const target = () => {};
    const options = {
      isValid: () => false,
      default: 'filtered'
    };
    assert.strictEqual(getValue(target, 'someprop', options), 'filtered');
  });

  it('should handle path as undefined', () => {
    const obj = { foo: 1 };
    assert.strictEqual(getValue(obj, undefined as any, { default: 'none' }), 'none');
  });

  it('should treat splitChar as falsy and default to \'.\'', () => {
    const obj = { foo: { bar: 2 } };
    const options = { separator: undefined };
    assert.strictEqual(getValue(obj, 'foo.bar', options), 2);
  });

  it('should handle options not being an object (number, string, boolean)', () => {
    const obj = {};
    assert.strictEqual(getValue(obj, 'x', 0), 0);
    assert.strictEqual(getValue(obj, 'x', false), false);
    assert.strictEqual(getValue(obj, 'x', null), undefined);
  });
});