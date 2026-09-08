const frequencySort = require('./sort-characters-by-frequency');

describe('frequencySort', () => {
  test('sorts characters by descending frequency', () => {
    const result = frequencySort('tree');
    expect(result).toMatch(/ee/);
    expect(result).toMatch(/t|r/);
    expect(result.length).toBe(4);
  });

  test('distinct characters', () => {
    expect(frequencySort('abc')).toMatch(/[abc]{3}/);
  });

  test('empty string', () => {
    expect(frequencySort('')).toBe('');
  });

  test('all same character', () => {
    expect(frequencySort('aaa')).toBe('aaa');
  });

  test('mixed frequency', () => {
    const s = 'cccaaa';
    const out = frequencySort(s);
    expect(['cccaaa', 'aaaccc']).toContain(out);
  });
});