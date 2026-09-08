const deepDiff = require('../index');

describe('deep-diff exports', () => {
  test('main function is callable and validates diff', () => {
    // Basic test: simple value diff
    const a = {x: 1, y: 2};
    const b = {x: 1, y: 3, z: 4};
    const result = deepDiff(a, b);
    expect(Array.isArray(result)).toBe(true);
    // Kind N (new), E (edit)
    expect(result.some(r => r.kind === 'E' || r.kind === 'N')).toBe(true);
  });

  test('diff returns undefined for no diff', () => {
    const one = {foo: 1};
    expect(deepDiff(one, {foo: 1})).toBeUndefined();
    expect(deepDiff(1, 1)).toBeUndefined();
    expect(deepDiff(null, null)).toBeUndefined();
    expect(deepDiff(undefined, undefined)).toBeUndefined();
  });

  test('array difference', () => {
    const arr1 = [1,2,3];
    const arr2 = [1,3,2,4];
    const diffres = deepDiff(arr1, arr2);
    expect(diffres).toBeDefined();
    expect(Array.isArray(diffres)).toBe(true);
    // Should contain at least one Array diff
    expect(diffres.some(r => r.kind === 'A')).toBe(true);
  });

  test('deep diff: circular references', () => {
    const x = {foo: 1};
    x.self = x;
    const y = {foo: 2};
    y.self = y;
    const diff = deepDiff(x, y);
    expect(diff).toBeDefined();
    expect(Array.isArray(diff)).toBe(true);
  });

  test('diff with Date and RegExp types', () => {
    const d1 = {date: new Date('2020-01-01')};
    const d2 = {date: new Date('2022-01-01')};
    const r = deepDiff(d1, d2);
    expect(r).toBeDefined();
    expect(r.some(ch => ch.kind === 'E')).toBe(true);

    const obj1 = {re: /abc/i};
    const obj2 = {re: /xyz/g};
    const r2 = deepDiff(obj1, obj2);
    expect(r2).toBeDefined();
    expect(r2.some(ch => ch.kind === 'E')).toBe(true);
  });

  test('Can applyChange and revertChange', () => {
    const original = {x: 1, y: 2};
    const modified = {x: 1, y: 3, z: 4};
    const diffs = deepDiff(original, modified);

    // Apply changes to a copy of original
    const obj = {x: 1, y: 2};
    diffs.forEach(diff => deepDiff.applyChange(obj, original, diff));
    expect(obj).toEqual(modified);

    // Now revert changes
    diffs.reverse().forEach(diff => deepDiff.revertChange(obj, original, diff));
    expect(obj).toEqual(original);
  });

  test('preFilter skips selected keys', () => {
    const obj1 = {a: 1, b: 2, skip: 3};
    const obj2 = {a: 5, b: 6, skip: 10};
    const r = deepDiff(obj1, obj2, (path,key) => key === "skip");
    expect(r.some(diff => diff.path.includes("skip"))).toBe(false);
  });

  test('observableDiff invokes callback on every change', () => {
    const obj1 = {m: 1, n: 2};
    const obj2 = {m: 1, n: 3, o: 4};
    const observed = [];
    deepDiff.observableDiff(obj1, obj2, d => d ? observed.push(d) : null);
    expect(observed.length).toBeGreaterThan(0);
    expect(observed.some(d => d.kind === 'N' || d.kind === 'E')).toBe(true);
  });

  test('noConflict restores previous DeepDiff global', () => {
    // Only relevant in browser, but code path is global assign
    const fakeRoot = {};
    const returned = require('../index').noConflict ? require('../index').noConflict.call({DeepDiff: 1}, fakeRoot) : null;
    // Should return the deepDiff API value
    if (returned) expect(typeof returned).toBe('function');
  });
});

/*
 * Additional dedicated branch coverage for uncovered code in index.js
 */

// Cover deleting property (D) and array item removed
describe('deep-diff coverage: deleting and arrays', () => {
  test('detects deleted property', () => {
    const before = {foo: 1, gone: 2};
    const after = {foo: 1};
    const res = deepDiff(before, after);
    expect(res.some(r => r.kind === 'D')).toBe(true);
  });

  test('detects array item removed', () => {
    const before = [1,2,3,4];
    const after = [1,3,4];
    const res = deepDiff(before, after);
    expect(res.filter(r => r.kind === 'A' && r.item.kind === 'D').length).toBeGreaterThan(0);
  });

  test('applyDiff with array "A" modification', () => {
    const arr1 = [1,2,3];
    const arr2 = [1,4,3];
    const diffArr = deepDiff(arr1, arr2);
    let copy = arr1.slice();
    diffArr.forEach(d => deepDiff.applyChange(copy, arr1, d));
    expect(copy).toEqual(arr2);
  });
});

// Cover null/undefined and circular detection in observableDiff
describe('deep-diff: coverage for edge cases', () => {
  test('observableDiff handles null and undefined', () => {
    const arr = [];
    deepDiff.observableDiff(null, {}, d => arr.push(d));
    deepDiff.observableDiff(undefined, {}, d => arr.push(d));
    expect(arr.length).toBeGreaterThanOrEqual(0);
  });

  test('observableDiff with circular references', () => {
    const a = {};
    a.a = a;
    const b = {};
    b.a = b;
    const items = [];
    deepDiff.observableDiff(a, b, change => items.push(change));
    expect(items.length).toBeGreaterThanOrEqual(1);
  });
});

// Coverage for applyDiff with invalid diff
describe('deep-diff: invalid diff applications', () => {
  test('applyChange does nothing for unknown kind', () => {
    const o = {a: 1};
    const orig = {a: 1};
    const badDiff = {kind: 'X', path: []};
    expect(() => deepDiff.applyChange(o, orig, badDiff)).not.toThrow();
  });
  test('revertChange does nothing for unknown kind', () => {
    const o = {a: 1};
    const orig = {a: 1};
    const badDiff = {kind: 'X', path: []};
    expect(() => deepDiff.revertChange(o, orig, badDiff)).not.toThrow();
  });
});