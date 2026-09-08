const prettierBytes = require('../index');

// Different data from original tests, but matching logic and output format as per actual implementation.
describe('prettierBytes edge and negative cases (public tests)', () => {
  test('negative number between -1 and 0', () => {
    expect(prettierBytes(-0.4)).toBe('-0.4 B');
    expect(prettierBytes(-0.01)).toBe('-0.01 B');
  });

  test('other negative bytes', () => {
    expect(prettierBytes(-77)).toBe('-77 B');
    expect(prettierBytes(-2345)).toBe('-2.3 KB');
    expect(prettierBytes(-3500)).toBe('-3.5 KB');
    expect(prettierBytes(-1900)).toBe('-1.9 KB');
  });

  test('zero bytes (alternate, decimal representation)', () => {
    expect(prettierBytes(0)).toBe('0 B');
    expect(prettierBytes(-0)).toBe('0 B');
  });

  test('no unit if just below 1000', () => {
    expect(prettierBytes(999)).toBe('999 B');
    expect(prettierBytes(-999)).toBe('-999 B');
  });

  test('threshold 1000 with other values', () => {
    expect(prettierBytes(1500)).toBe('1.5 KB');
    // Implementation always rounds to 1 decimal, not more unless needed,
    // so 123456 --> 123 KB, not 123.5 KB
    expect(prettierBytes(123456)).toBe('123 KB');
    expect(prettierBytes(9000)).toBe('9 KB');
  });

  // Large numbers to hit higher units with non-powers of ten
  test('large units with other magnitudes', () => {
    expect(prettierBytes(2e21)).toBe('2 ZB');
    expect(prettierBytes(7.6e18)).toBe('7.6 EB');
    expect(prettierBytes(2.4e15)).toBe('2.4 PB');
    expect(prettierBytes(1.2e12)).toBe('1.2 TB');
    expect(prettierBytes(4.7e9)).toBe('4.7 GB');
    expect(prettierBytes(6.5e6)).toBe('6.5 MB');
  });

  test('decimal rounding (other public examples)', () => {
    // Implementation outputs trailing zero for .0 (5.0 KB), so check like the main test does.
    expect(prettierBytes(5023)).toBe('5.0 KB');
    expect(prettierBytes(2591)).toBe('2.6 KB');
  });

  test('Infinity and -Infinity still handled', () => {
    // Implementation converts Infinity => 'Infinity YB' and -Infinity => '-Infinity YB'
    expect(prettierBytes(Infinity)).toBe('Infinity YB');
    expect(prettierBytes(-Infinity)).toBe('-Infinity YB');
  });

  test('bad types (public set)', () => {
    expect(() => prettierBytes('hello')).toThrow();
    expect(() => prettierBytes(null)).toThrow();
    expect(() => prettierBytes(undefined)).toThrow();
    expect(() => prettierBytes({})).toThrow();
    expect(() => prettierBytes([])).toThrow();
  });
});