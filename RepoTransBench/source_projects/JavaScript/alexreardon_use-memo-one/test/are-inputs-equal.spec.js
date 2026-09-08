// @flow
import areInputsEqual from '../src/are-inputs-equal';

describe('areInputsEqual', () => {
  it('returns true when both arrays are empty', () => {
    expect(areInputsEqual([], [])).toBe(true);
  });

  it('returns false when arrays have different lengths', () => {
    expect(areInputsEqual([1], [])).toBe(false);
    expect(areInputsEqual([], [1])).toBe(false);
    expect(areInputsEqual([1,2], [1])).toBe(false);
  });

  it('returns true for shallow equal arrays', () => {
    expect(areInputsEqual([1, 2, 3], [1, 2, 3])).toBe(true);
    expect(areInputsEqual(['a', 'b'], ['a', 'b'])).toBe(true);
    const obj = {};
    expect(areInputsEqual([obj], [obj])).toBe(true);
  });

  it('returns false if any value differs (shallow)', () => {
    expect(areInputsEqual([1, 2, 3], [1, 2, 4])).toBe(false);
    expect(areInputsEqual([{x:1}], [{x:1}])).toBe(false); // different references
    expect(areInputsEqual([undefined], [null])).toBe(false);
    expect(areInputsEqual([NaN], [NaN])).toBe(false); // NaN !== NaN
  });

  it('returns true for same reference arrays', () => {
    const arr = [1, 2];
    expect(areInputsEqual(arr, arr)).toBe(true);
  });

  it('returns false for shallow-equal-but-different-references objects', () => {
    expect(areInputsEqual([{ x: 1 }], [{ x: 1 }])).toBe(false);
  });

  it('handles complex edge cases', () => {
    class Foo { constructor(v) { this.v = v; } }
    const a = new Foo(1);
    const b = new Foo(1);
    expect(areInputsEqual([a], [a])).toBe(true);
    expect(areInputsEqual([a], [b])).toBe(false);
    expect(areInputsEqual([1, "a", null], [1, "a", null])).toBe(true);
    expect(areInputsEqual([1, 2], [1, 2, 3])).toBe(false);
  });
});