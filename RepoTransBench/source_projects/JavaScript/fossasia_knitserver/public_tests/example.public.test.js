const { add, subtract, isPositive, classify } = require('../src/example');

describe('add', () => {
  test('adds positive numbers', () => {
    expect(add(10, 3)).toBe(13);
  });

  test('adds negative numbers', () => {
    expect(add(-3, -5)).toBe(-8);
  });
});

describe('subtract', () => {
  test('subtracts numbers', () => {
    expect(subtract(8, 3)).toBe(5);
  });

  test('throws error on invalid arguments', () => {
    expect(() => subtract({}, 2)).toThrow("Invalid arguments");
  });
});

describe('isPositive', () => {
  test('returns true for positive number', () => {
    expect(isPositive(42)).toBe(true);
  });
  test('returns false for zero', () => {
    expect(isPositive(0)).toBe(false);
  });
  test('returns false for negative', () => {
    expect(isPositive(-99)).toBe(false);
  });
  test('returns false for non-number', () => {
    expect(isPositive([1,2,3])).toBe(false);
  });
});

describe('classify', () => {
  test('returns "positive" for >0', () => {
    expect(classify(99)).toBe("positive");
  });
  test('returns "negative" for <0', () => {
    expect(classify(-100)).toBe("negative");
  });
  test('returns "zero" for 0', () => {
    expect(classify(0)).toBe("zero");
  });
  test('returns "not a number" for NaN', () => {
    expect(classify(undefined)).toBe("not a number");
  });
});