const { add, max } = require('../src/sample');

describe('add', () => {
  test('adds two positive numbers', () => {
    expect(add(2, 4)).toBe(6);
  });
  test('adds a negative and positive number', () => {
    expect(add(-5, 3)).toBe(-2);
  });
  test('adds two zeros', () => {
    expect(add(0, 0)).toBe(0);
  });
});

describe('max', () => {
  test('returns the maximum value in a positive array', () => {
    expect(max([1, 3, 2])).toBe(3);
  });
  test('returns the maximum value in a negative array', () => {
    expect(max([-1, -3, -2])).toBe(-1);
  });
  test('returns null for empty array', () => {
    expect(max([])).toBeNull();
  });
  test('returns null for undefined', () => {
    expect(max(undefined)).toBeNull();
  });
  test('returns the single value for single-element array', () => {
    expect(max([42])).toBe(42);
  });
});