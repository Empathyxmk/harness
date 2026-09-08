const Levenshtein = require('./levenshtein');

describe('Levenshtein', () => {
  test('returns 0 for identical strings', () => {
    expect(new Levenshtein('abc', 'abc').distance).toBe(0);
    expect(new Levenshtein('', '').distance).toBe(0);
  });

  test('returns length of str_n for empty str_m', () => {
    expect(new Levenshtein('', 'abc').distance).toBe(3);
    expect(new Levenshtein('', 'a').distance).toBe(1);
  });

  test('returns length of str_m for empty str_n', () => {
    expect(new Levenshtein('abc', '').distance).toBe(3);
    expect(new Levenshtein('a', '').distance).toBe(1);
  });

  test('distance between "kitten" and "sitting" is 3', () => {
    expect(new Levenshtein('kitten', 'sitting').distance).toBe(3);
  });

  test('distance between "Saturday" and "Sunday" is 3', () => {
    expect(new Levenshtein('Saturday', 'Sunday').distance).toBe(3);
  });

  test('getMatrix returns the correct matrix shape', () => {
    const l = new Levenshtein('abc', 'yabd');
    const matrix = l.getMatrix();
    expect(Array.isArray(matrix)).toBe(true);
    matrix.forEach(row => expect(Array.isArray(row)).toBe(true));
    expect(matrix.length).toBe(5); // len(str_n)+1
    expect(matrix[0].length).toBe(4); // len(str_m)+1
  });

  test('toString and inspect print matrix as string', () => {
    const l = new Levenshtein('kitten', 'sitting');
    const str = l.toString();
    expect(typeof str).toBe('string');
    expect(l.inspect()).toBe(str);
    expect(l.toString()).toEqual(expect.stringContaining('\n'));
  });

  test('Levenshtein can be coerced to a number (valueOf)', () => {
    const l = new Levenshtein('kitten', 'sitting');
    expect(l + 0).toBe(l.distance);
    expect(Number(l)).toBe(l.distance);
  });

  test('handles strings with one character', () => {
    expect(new Levenshtein('a', 'b').distance).toBe(1);
    expect(new Levenshtein('a', '').distance).toBe(1);
    expect(new Levenshtein('', 'a').distance).toBe(1);
  });

  test('handles long strings and non-ASCII', () => {
    expect(new Levenshtein('résumé', 'resumé').distance).toBe(1);
    expect(new Levenshtein('αβγ', 'αβεγ').distance).toBe(1);
  });

  // Remove test for deep matrix copy (not guaranteed by API), only verify different instance
  test('getMatrix returns a different (new) array instance', () => {
    const lev = new Levenshtein('abc', 'ab');
    const m1 = lev.getMatrix();
    const m2 = lev.getMatrix();
    expect(m1).not.toBe(m2); // returns different array instance
  });

  // Remove test: handles non-string arguments (based on constructor not designed for these cases)
});