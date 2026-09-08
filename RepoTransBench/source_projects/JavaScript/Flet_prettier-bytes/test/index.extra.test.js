const prettierBytes = require('../');

describe('prettierBytes edge and negative cases', () => {
  // Negative numbers
  test('negative number below 1', () => {
    expect(prettierBytes(-0.2)).toBe('-0.2 B');
  });

  test('negative bytes', () => {
    expect(prettierBytes(-45)).toBe('-45 B');
    expect(prettierBytes(-1500)).toBe('-1.5 KB');
    expect(prettierBytes(-2510)).toBe('-2.5 KB');
    expect(prettierBytes(-1000)).toBe('-1 KB');
  });

  // Zero
  test('zero bytes', () => {
    expect(prettierBytes(0)).toBe('0 B');
  });

  // Numbers just less than 1000 to test no unit change
  test('no unit if under 1000', () => {
    expect(prettierBytes(999)).toBe('999 B');
  });

  // Numbers just above 1000
  test('threshold 1000', () => {
    expect(prettierBytes(1000)).toBe('1 KB');
    expect(prettierBytes(1001)).toBe('1.0 KB');
    expect(prettierBytes(1500)).toBe('1.5 KB');
    expect(prettierBytes(1100)).toBe('1.1 KB');
    expect(prettierBytes(2000)).toBe('2 KB');
    expect(prettierBytes(9900)).toBe('9.9 KB');
    expect(prettierBytes(10000)).toBe('10 KB');
  });

  // Large numbers to hit higher units
  test('large units', () => {
    expect(prettierBytes(1e24)).toBe('1 YB');
    expect(prettierBytes(1e21)).toBe('1 ZB');
    expect(prettierBytes(1e18)).toBe('1 EB');
    expect(prettierBytes(1e15)).toBe('1 PB');
    expect(prettierBytes(1e12)).toBe('1 TB');
    expect(prettierBytes(1e9)).toBe('1 GB');
    expect(prettierBytes(1e6)).toBe('1 MB');
    expect(prettierBytes(1e3)).toBe('1 KB');
  });

  // Decimal handling: just above/below thresholds for decimals
  test('decimal rounding', () => {
    expect(prettierBytes(1234)).toBe('1.2 KB');
    expect(prettierBytes(12345)).toBe('12 KB');
    expect(prettierBytes(10000)).toBe('10 KB');
    expect(prettierBytes(10100)).toBe('10 KB');
    expect(prettierBytes(10900)).toBe('11 KB');
    expect(prettierBytes(100900)).toBe('101 KB');
  });
  
  // Special numbers: Infinity is valid input, should NOT throw
  test('Infinity returns value', () => {
    expect(prettierBytes(Infinity)).toBe('Infinity YB');
    expect(prettierBytes(-Infinity)).toBe('-Infinity YB');
  });

  // non-number, null, object, array
  test('non-number argument types', () => {
    expect(() => prettierBytes(undefined)).toThrow(TypeError);
    expect(() => prettierBytes({})).toThrow(TypeError);
    expect(() => prettierBytes([])).toThrow(TypeError);
    expect(() => prettierBytes(null)).toThrow(TypeError);
    expect(() => prettierBytes(false)).toThrow(TypeError);
  });
});