const Levenshtein = require('../lib/levenshtein');

describe('Levenshtein (public)', () => {
  test('returns 0 for identical strings (different inputs)', () => {
    expect(new Levenshtein('hello', 'hello').distance).toBe(0);
    expect(new Levenshtein('123', '123').distance).toBe(0);
  });

  test('returns length of str_n for empty str_m (different inputs)', () => {
    expect(new Levenshtein('', 'xyz').distance).toBe(3);
    expect(new Levenshtein('', 'longer').distance).toBe(6);
  });

  test('returns length of str_m for empty str_n (different inputs)', () => {
    expect(new Levenshtein('test', '').distance).toBe(4);
    expect(new Levenshtein('foo', '').distance).toBe(3);
  });

  test('distance between "flaw" and "lawn" is 2', () => {
    expect(new Levenshtein('flaw', 'lawn').distance).toBe(2);
  });

  test('distance between "gumbo" and "gambol" is 2', () => {
    expect(new Levenshtein('gumbo', 'gambol').distance).toBe(2);
  });

  test('getMatrix returns the correct matrix shape (different inputs)', () => {
    const l = new Levenshtein('abcd', 'efgh');
    const matrix = l.getMatrix();
    expect(Array.isArray(matrix)).toBe(true);
    matrix.forEach(row => expect(Array.isArray(row)).toBe(true));
    expect(matrix.length).toBe(5); // len(str_n)+1
    expect(matrix[0].length).toBe(5); // len(str_m)+1
  });

  test('toString and inspect print matrix as string (different inputs)', () => {
    const l = new Levenshtein('banana', 'canada');
    const str = l.toString();
    expect(typeof str).toBe('string');
    expect(l.inspect()).toBe(str);
    expect(l.toString()).toEqual(expect.stringContaining('\n'));
  });

  test('Levenshtein can be coerced to a number (valueOf)', () => {
    const l = new Levenshtein('hey', 'hay');
    expect(l + 0).toBe(l.distance);
    expect(Number(l)).toBe(l.distance);
  });

  test('handles strings with one character (different inputs)', () => {
    expect(new Levenshtein('x', 'y').distance).toBe(1);
    expect(new Levenshtein('z', '').distance).toBe(1);
    expect(new Levenshtein('', 'q').distance).toBe(1);
  });

  test('handles long strings and non-ASCII (different inputs)', () => {
    expect(new Levenshtein('café', 'caffè').distance).toBe(2);
    expect(new Levenshtein('друг', 'дуга').distance).toBe(2);
  });

  test('getMatrix returns a different (new) array instance', () => {
    const lev = new Levenshtein('test', 'best');
    const m1 = lev.getMatrix();
    const m2 = lev.getMatrix();
    expect(m1).not.toBe(m2); // returns different array instance
  });
});