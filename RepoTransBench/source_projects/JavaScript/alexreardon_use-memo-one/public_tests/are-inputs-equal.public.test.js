// @flow
import areInputsEqual from '../src/are-inputs-equal';

describe('areInputsEqual - public', () => {
  it('returns true for two empty arrays', () => {
    expect(areInputsEqual([], [])).toBe(true);
  });

  it('returns false for arrays of different lengths', () => {
    expect(areInputsEqual([1, 2], [1, 2, 3])).toBe(false);
  });

  it('returns false if one element is different', () => {
    expect(areInputsEqual([5, 'c', null], [5, 'c', 0])).toBe(false);
  });

  it('returns true if the arrays contain same references for objects', () => {
    const ref = { b: 2 };
    expect(areInputsEqual([ref, 8], [ref, 8])).toBe(true);
  });

  it('returns false for deep but non-reference equality on objects', () => {
    expect(areInputsEqual([{ p: 2 }], [{ p: 2 }])).toBe(false);
  });
});