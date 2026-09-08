const dlv = require('../dlv.js');

describe('dlv (public data)', () => {
  test('retrieves a deeply nested value (different path/data)', () => {
    const data = {x: {y: {z: 99}}};
    expect(dlv(data, 'x.y.z')).toBe(99);
    expect(dlv(data, ['x','y','z'])).toBe(99);
  });

  test('returns default value if not found (new property/default)', () => {
    const data = {foo: 9};
    expect(dlv(data, 'bar', 42)).toBe(42);
    expect(dlv(data, ['bar'], null)).toBe(null);
  });

  test('returns undefined when not found and no default (unused key)', () => {
    const data = {hello: 'world'};
    expect(dlv(data, 'absent')).toBe(undefined);
  });

  test('handles falsy values (new falsy and nulls)', () => {
    const data = {a: '', b: false, c: 0, d: undefined};
    expect(dlv(data, 'a')).toBe('');
    expect(dlv(data, 'b')).toBe(false);
    expect(dlv(data, 'c')).toBe(0);
    expect(dlv(data, 'd')).toBe(undefined);
  });

  test('handles array indices (different data/indices)', () => {
    const data = {arr: [10, 20, {x: 30}]};
    expect(dlv(data, 'arr.0')).toBe(10);
    expect(dlv(data, ['arr','1'])).toBe(20);
    expect(dlv(data, 'arr.2.x')).toBe(30);
    expect(dlv(data, ['arr','2','x'])).toBe(30);
  });

  test('handles numeric keys as string only (diff objects/arrays)', () => {
    const data = {1: 'b'};
    expect(dlv(data, '1')).toBe('b');
    expect(dlv(data, ['1'])).toBe('b');
    expect(dlv([5,6,7], '2')).toBe(7);
  });

  test('handles empty path (new object)', () => {
    const data = {foo:2};
    expect(dlv(data, '')).toBe(undefined);
    expect(dlv(data, [])).toBe(data);
  });

  test('handles non-object root (change value and type)', () => {
    expect(dlv(null, 'q', 'fallback')).toBe('fallback');
    expect(dlv(undefined, ['x'], 'abc')).toBe('abc');
    expect(dlv(100, 'y', 'red')).toBe('red');
    expect(dlv('hello', ['0'], 'zero')).toBe('zero');
  });

  test('should handle key as object (not splittable string) - different key/value', () => {
    const obj = { b: 2 };
    expect(dlv(obj, {}, 'missing')).toEqual({ b: 2 });
  });

  test('should handle arrays as objects (different array/data)', () => {
    expect(dlv([9,8,7], 2, 'none')).toEqual([9,8,7]); // when path is not array/string, returns root
    expect(dlv([3,4,5], ['2'])).toBe(5);
  });

  test('should treat keys with dots as single key in array form (change)', () => {
    const obj = { 'x.y': { w: 10 } };
    expect(dlv(obj, ['x.y','w'])).toBe(10);
    expect(dlv(obj, 'x.y.w')).toBe(undefined);
  });

  test('should return default for missing intermediate object (new key data)', () => {
    const data = { b: 2 };
    expect(dlv(data, 'b.z.y', 'out')).toBe('out');
    expect(dlv(data, ['b','z','y'], 'miss')).toBe('miss');
  });

  test('should find value when 0 is key (different structure)', () => {
    const data = { b: {0: 'value0'} };
    expect(dlv(data, ['b', '0'])).toBe('value0');
    expect(dlv([{name:'a'}], '0.name')).toBe('a');
  });

  test('should work on primitive root with empty path (change primitive)', () => {
    expect(dlv(true, [], 'no')).toBe(true);
    expect(dlv('xyz', [], 'no')).toBe('xyz');
  });

  test('should return default when root is undefined/null/primitive and key is not empty', () => {
    expect(dlv(undefined, ['baz'], 'qux')).toBe('qux');
    expect(dlv(null, ['baz'], 777)).toBe(777);
    expect(dlv(1, ['foo'], false)).toBe(false);
  });

  test('should return undefined for missing keys if no default (diff key/array)', () => {
    expect(dlv({}, ['absent'])).toBe(undefined);
    expect(dlv([], ['4'])).toBe(undefined);
  });

  test('should support symbol keys (change symbol description)', () => {
    const s = Symbol('another');
    const obj = { [s]: 7 };
    expect(dlv(obj, [s], 11)).toBe(7);
  });

  test('should return array for empty string key path on array', () => {
    expect(dlv([9,8,7], '')).toBe(undefined);
    expect(dlv([9,8,7], [])).toEqual([9,8,7]);
  });

  test('should return default when traversing leaves (different obj/default)', () => {
    expect(dlv({b:{c:5}}, ['b','c','d'], 'Leaf')).toBe('Leaf');
    expect(dlv({b: null}, ['b','z'], 'Done')).toBe('Done');
  });
});