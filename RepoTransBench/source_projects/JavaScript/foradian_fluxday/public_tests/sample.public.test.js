const { add, max } = require('../src/sample');

describe('add', () => {
  test('adds two positive numbers', () => {
    expect(add(7, 10)).toBe(17);
  });
  test('adds a negative and positive number', () => {
    expect(add(-8, 4)).toBe(-4);
  });
  test('adds two zeros', () => {
    expect(add(0, 0)).toBe(0);
  });
});

describe('max', () => {
  test('returns the maximum value in a positive array', () => {
    expect(max([5, 8, 7])).toBe(8);
  });
  test('returns the maximum value in a negative array', () => {
    expect(max([-10, -5, -8])).toBe(-5);
  });
  test('returns null for empty array', () => {
    expect(max([])).toBeNull();
  });
  test('returns null for undefined', () => {
    expect(max(undefined)).toBeNull();
  });
  test('returns the single value for single-element array', () => {
    expect(max([99])).toBe(99);
  });
}
);