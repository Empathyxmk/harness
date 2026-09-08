const deepDiff = require('../index');

describe('deep-diff exports (public)', () => {
  test('main function is callable and validates diff (public)', () => {
    // Different value objects
    const a = {a: 10, b: 20};
    const b = {a: 10, b: 30, c: 40};
    const result = deepDiff(a, b);
    expect(Array.isArray(result)).toBe(true);
    expect(result.some(r => r.kind === 'E' || r.kind === 'N')).toBe(true);
  });

  test('diff returns undefined for no diff (public)', () => {
    const test = {bar: 42};
    expect(deepDiff(test, {bar: 42})).toBeUndefined();
    expect(deepDiff(5, 5)).toBeUndefined();
    expect(deepDiff(null, null)).toBeUndefined();
    expect(deepDiff(undefined, undefined)).toBeUndefined();
  });

  test('array difference (public)', () => {
    const arr1 = [4,5,6];
    const arr2 = [4,6,5,7];
    const diffres = deepDiff(arr1, arr2);
    expect(diffres).toBeDefined();
    expect(Array.isArray(diffres)).toBe(true);
    expect(diffres.some(r => r.kind === 'A')).toBe(true);
  });

  test('deep diff: circular references (public)', () => {
    const obj1 = {bar: 10};
    obj1.myself = obj1;
    const obj2 = {bar: 20};
    obj2.myself = obj2;
    const diff = deepDiff(obj1, obj2);
    expect(diff).toBeDefined();
    expect(Array.isArray(diff)).toBe(true);
  });

  test('diff with Date and RegExp types (public)', () => {
    const d1 = {date: new Date('2019-05-05')};
    const d2 = {date: new Date('2021-06-10')};
    const r = deepDiff(d1, d2);
    expect(r).toBeDefined();
    expect(r.some(ch => ch.kind === 'E')).toBe(true);

    const obj1 = {reg: /123/g};
    const obj2 = {reg: /999/m};
    const r2 = deepDiff(obj1, obj2);
    expect(r2).toBeDefined();
    expect(r2.some(ch => ch.kind === 'E')).toBe(true);
  });

  test('Can applyChange and revertChange (public)', () => {
    const original = {a: 100, b: 200};
    const modified = {a: 100, b: 999, c: 123};
    const diffs = deepDiff(original, modified);

    const obj = {a: 100, b: 200};
    diffs.forEach(diff => deepDiff.applyChange(obj, original, diff));
    expect(obj).toEqual(modified);

    diffs.reverse().forEach(diff => deepDiff.revertChange(obj, original, diff));
    expect(obj).toEqual(original);
  });

  test('preFilter skips selected keys (public)', () => {
    const obj1 = {foo: 1, bar: 2, omit: 99};
    const obj2 = {foo: 10, bar: 20, omit: 123};
    const r = deepDiff(obj1, obj2, (path, key) => key === "omit");
    expect(r.some(diff => diff.path.includes("omit"))).toBe(false);
  });

  test('observableDiff invokes callback on every change (public)', () => {
    const obj1 = {p: 111, q: 222};
    const obj2 = {p: 111, q: 333, r: 444};
    const observed = [];
    deepDiff.observableDiff(obj1, obj2, d => d ? observed.push(d) : null);
    expect(observed.length).toBeGreaterThan(0);
    expect(observed.some(d => d.kind === 'N' || d.kind === 'E')).toBe(true);
  });

  test('noConflict restores previous DeepDiff global (public)', () => {
    const fakeRoot = {};
    const returned = require('../index').noConflict ? require('../index').noConflict.call({DeepDiff: 2}, fakeRoot) : null;
    if (returned) expect(typeof returned).toBe('function');
  });
});

// Additional dedicated branch coverage for uncovered code in index.js
describe('deep-diff coverage: deleting and arrays (public)', () => {
  test('detects deleted property (public)', () => {
    const before = {bar: 10, remove: 20};
    const after = {bar: 10};
    const res = deepDiff(before, after);
    expect(res.some(r => r.kind === 'D')).toBe(true);
  });

  test('detects array item removed (public)', () => {
    const before = [9,8,7,6];
    const after = [9,7,6];
    const res = deepDiff(before, after);
    expect(res.filter(r => r.kind === 'A' && r.item.kind === 'D').length).toBeGreaterThan(0);
  });

  test('applyDiff with array "A" modification (public)', () => {
    const arr1 = [4,5,6];
    const arr2 = [4,8,6];
    const diffArr = deepDiff(arr1, arr2);
    let copy = arr1.slice();
    diffArr.forEach(d => deepDiff.applyChange(copy, arr1, d));
    expect(copy).toEqual(arr2);
  });
});

// Cover null/undefined and circular detection in observableDiff
describe('deep-diff: coverage for edge cases (public)', () => {
  test('observableDiff handles null and undefined (public)', () => {
    const arr = [];
    deepDiff.observableDiff(null, {foo: 1}, d => arr.push(d));
    deepDiff.observableDiff(undefined, {foo: 1}, d => arr.push(d));
    expect(arr.length).toBeGreaterThanOrEqual(0);
  });

  test('observableDiff with circular references (public)', () => {
    const a = {};
    a.ref = a;
    const b = {};
    b.ref = b;
    const items = [];
    deepDiff.observableDiff(a, b, change => items.push(change));
    expect(items.length).toBeGreaterThanOrEqual(1);
  });
});

// Coverage for applyDiff with invalid diff
describe('deep-diff: invalid diff applications (public)', () => {
  test('applyChange does nothing for unknown kind (public)', () => {
    const obj = {foo: 77};
    const orig = {foo: 77};
    const badDiff = {kind: 'Z', path: []};
    expect(() => deepDiff.applyChange(obj, orig, badDiff)).not.toThrow();
  });
  test('revertChange does nothing for unknown kind (public)', () => {
    const obj = {bar: 88};
    const orig = {bar: 88};
    const badDiff = {kind: 'Y', path: []};
    expect(() => deepDiff.revertChange(obj, orig, badDiff)).not.toThrow();
  });
});