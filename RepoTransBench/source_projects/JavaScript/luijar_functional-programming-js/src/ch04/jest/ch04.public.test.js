/**
 * Public test for ch04/helper.js with different input/output
 */

const R = require('ramda');

describe('Chapter 4 public helper tests', () => {
  test('should reverse and uppercase a new string (public)', () => {
    const reverseUpper = R.compose(
      s => s.toUpperCase(),
      s => s.split('').reverse().join('')
    );
    expect(reverseUpper('alphabet')).toBe('TEBAPHLA');
  });

  test('should map a function over an array with new data (public)', () => {
    const double = n => n * 2;
    expect([4, 6, 8].map(double)).toEqual([8, 12, 16]);
  });
});