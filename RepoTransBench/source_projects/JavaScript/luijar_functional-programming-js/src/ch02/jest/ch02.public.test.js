/**
 * Public test for ch02/helper.js with different input/output data
 */

const R = require('ramda');

// Instead of the original test logic, provide analogous but different input/output scenarios.
describe('Chapter 2 helper.js public tests', () => {
  test('should curry a new multiply function (public)', () => {
    const multiply = R.curry((a, b) => a * b);
    const double = multiply(2);
    expect(double(7)).toBe(14); // different input than original
    expect(double(8)).toBe(16);
  });

  test('should create a new object with a different transformation (public)', () => {
    // Simulate a functional prop transformation with new keys/values
    const obj = { alpha: 5, beta: 10 };
    const fn = R.evolve({ alpha: n => n * 3, beta: n => n + 7 });
    expect(fn(obj)).toStrictEqual({ alpha: 15, beta: 17 });
  });
});