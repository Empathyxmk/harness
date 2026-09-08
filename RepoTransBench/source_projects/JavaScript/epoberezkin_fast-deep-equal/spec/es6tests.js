const equal = require('../es6/index');

describe('fast-deep-equal - es6/index.js', () => {
  it('should compare maps', () => {
    const m1 = new Map([['a',1],['b',2]]);
    const m2 = new Map([['a',1],['b',2]]);
    const m3 = new Map([['a',1],['b',3]]);
    const m4 = new Map([['a',1]]);
    expect(equal(m1, m2)).toBe(true);
    expect(equal(m1, m3)).toBe(false);
    expect(equal(m1, m4)).toBe(false);
    // keys mismatch
    const m5 = new Map([['a',2],['c',3]]);
    expect(equal(m1, m5)).toBe(false);
  });

  it('should compare sets', () => {
    const s1 = new Set([1,2,3]);
    const s2 = new Set([1,2,3]);
    const s3 = new Set([1,2]);
    const s4 = new Set([3,2,1]);
    expect(equal(s1, s2)).toBe(true);
    expect(equal(s1, s3)).toBe(false);
    expect(equal(s1, s4)).toBe(true); // set order doesn't matter
    // sets with different contents
    const s5 = new Set([1,2,4]);
    expect(equal(s1, s5)).toBe(false);
  });

  it('should compare typed arrays (ArrayBuffer views)', () => {
    const a = new Uint8Array([1,2,3]);
    const b = new Uint8Array([1,2,3]);
    const c = new Uint8Array([1,2,4]);
    expect(equal(a, b)).toBe(true);
    expect(equal(a, c)).toBe(false);
    // different types
    const d = new Uint16Array([1,2,3]);
    expect(equal(a, d)).toBe(false);
  });

  it('should compare normal ArrayBuffer views of zero length', () => {
    const a = new Uint8Array([]);
    const b = new Uint8Array([]);
    expect(equal(a, b)).toBe(true);
  });

  it('should compare nested Map/Set in object', () => {
    const m1 = new Map([['a', new Set([1])]]);
    const m2 = new Map([['a', new Set([1])]]);
    expect(equal(m1, m2)).toBe(true);
    const m3 = new Map([['a', new Set([2])]]);
    expect(equal(m1, m3)).toBe(false);
  });

  it('should fall back to normal equal logic', () => {
    expect(equal('a', 'a')).toBe(true);
    expect(equal(1, 2)).toBe(false);
    expect(equal({x:1}, {x:2})).toBe(false);
    expect(equal([1,2], [1,2])).toBe(true);
  });
});