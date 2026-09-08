const { add, subtract, isPositive, classify } = require('./example');

describe('add', () => {
  test('adds positive numbers', () => {
    expect(add(1, 2)).toBe(3);
  });

  test('adds negative numbers', () => {
    expect(add(-1, -1)).toBe(-2);
  });
});

describe('subtract', () => {
  test('subtracts numbers', () => {
    expect(subtract(5, 1)).toBe(4);
  });

  test('throws error on invalid arguments', () => {
    expect(() => subtract("a", 2)).toThrow("Invalid arguments");
  });
});

describe('isPositive', () => {
  test('returns true for positive number', () => {
    expect(isPositive(3)).toBe(true);
  });
  test('returns false for zero', () => {
    expect(isPositive(0)).toBe(false);
  });
  test('returns false for negative', () => {
    expect(isPositive(-10)).toBe(false);
  });
  test('returns false for non-number', () => {
    expect(isPositive("str")).toBe(false);
  });
});

describe('classify', () => {
  test('returns "positive" for >0', () => {
    expect(classify(5)).toBe("positive");
  });
  test('returns "negative" for <0', () => {
    expect(classify(-2)).toBe("negative");
  });
  test('returns "zero" for 0', () => {
    expect(classify(0)).toBe("zero");
  });
  test('returns "not a number" for NaN', () => {
    expect(classify(NaN)).toBe("not a number");
  });
});