const stringSimilarity = require('../src/index');

describe('string-similarity core API (public tests)', () => {
  test('compareTwoStrings: identical strings', () => {
    expect(stringSimilarity.compareTwoStrings('abc123', 'abc123')).toBe(1);
  });

  test('compareTwoStrings: completely different', () => {
    expect(stringSimilarity.compareTwoStrings('dog', 'cat')).toBe(0);
  });

  test('compareTwoStrings: partial overlap', () => {
    const result = stringSimilarity.compareTwoStrings('marvelous', 'marvel');
    expect(result).toBeGreaterThan(0);
    expect(result).toBeLessThan(1);
  });

  test('compareTwoStrings: empty strings', () => {
    expect(stringSimilarity.compareTwoStrings('', '')).toBe(1);
    expect(stringSimilarity.compareTwoStrings('test', '')).toBe(0);
    expect(stringSimilarity.compareTwoStrings('', 'test')).toBe(0);
  });

  test('findBestMatch: best match in array', () => {
    const main = "baker";
    const matches = ["maker", "faker", "taker", "baker"];
    const output = stringSimilarity.findBestMatch(main, matches);
    expect(output.bestMatch.target).toBe("baker");
    expect(Array.isArray(output.ratings)).toBe(true);
    expect(output.ratings.length).toBe(4);
  });

  test('findBestMatch: handles bad argument types', () => {
    expect(() => stringSimilarity.findBestMatch(undefined, null)).toThrow();
    expect(() => stringSimilarity.findBestMatch('world', undefined)).toThrow();
    expect(() => stringSimilarity.findBestMatch('world', 10)).toThrow();
    expect(() => stringSimilarity.findBestMatch('world', ['a', true])).toThrow();
    expect(() => stringSimilarity.findBestMatch('world', [])).toThrow();
  });
});