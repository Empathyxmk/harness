const stringSimilarity = require('./index');

describe('string-similarity core API', () => {
  test('compareTwoStrings: identical strings', () => {
    expect(stringSimilarity.compareTwoStrings('hello', 'hello')).toBe(1);
  });

  test('compareTwoStrings: completely different', () => {
    expect(stringSimilarity.compareTwoStrings('foo', 'bar')).toBe(0);
  });

  test('compareTwoStrings: partial overlap', () => {
    const result = stringSimilarity.compareTwoStrings('hello', 'yellow');
    expect(result).toBeGreaterThan(0);
    expect(result).toBeLessThan(1);
  });

  test('compareTwoStrings: empty strings', () => {
    expect(stringSimilarity.compareTwoStrings('', '')).toBe(1);
    expect(stringSimilarity.compareTwoStrings('nonempty', '')).toBe(0);
    expect(stringSimilarity.compareTwoStrings('', 'nonempty')).toBe(0);
  });

  test('findBestMatch: best match in array', () => {
    const main = "healed";
    const matches = ["edward", "sealed", "theatre", "healed"];
    const output = stringSimilarity.findBestMatch(main, matches);
    expect(output.bestMatch.target).toBe("healed");
    expect(Array.isArray(output.ratings)).toBe(true);
    expect(output.ratings.length).toBe(4);
  });

  test('findBestMatch: handles bad argument types', () => {
    expect(() => stringSimilarity.findBestMatch(null, undefined)).toThrow();
    expect(() => stringSimilarity.findBestMatch('hello', null)).toThrow();
    expect(() => stringSimilarity.findBestMatch('hello', 42)).toThrow();
    expect(() => stringSimilarity.findBestMatch('hello', ['a', 42])).toThrow();
    expect(() => stringSimilarity.findBestMatch('hello', [])).toThrow();
  });
});