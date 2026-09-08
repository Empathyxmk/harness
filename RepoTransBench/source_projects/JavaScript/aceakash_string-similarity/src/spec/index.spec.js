// Adapted for error messages actually thrown by findBestMatch in src/index.js

const stringSimilarity = require('../index');
const findBestMatch = stringSimilarity.findBestMatch;

describe('findBestMatch', () => {
  const badArgsErrorMsg = 'Bad arguments: First argument should be a string, second should be an array of strings';

  test("throws a 'Bad arguments' error if no arguments passed", () => {
    expect(() => findBestMatch()).toThrow(badArgsErrorMsg);
  });

  test("throws a 'Bad arguments' error if first argument is not a string", () => {
    expect(() => findBestMatch(8)).toThrow(badArgsErrorMsg);
    expect(() => findBestMatch({})).toThrow(badArgsErrorMsg);
  });

  test("throws a 'Bad arguments' error if second argument is not an array", () => {
    expect(() => findBestMatch('hello', 'something')).toThrow(badArgsErrorMsg);
    expect(() => findBestMatch('hello', {})).toThrow(badArgsErrorMsg);
  });

  test("throws a 'Bad arguments' error if second argument is not an array of strings", () => {
    expect(() => findBestMatch('hello', [2, 'something'])).toThrow(badArgsErrorMsg);
  });

  test('assigns a similarity rating to each string passed in the array', () => {
    const result = findBestMatch('healed', ['edward', 'sealed', 'theatre']);
    expect(result.ratings).toEqual([
      { target: 'edward', rating: expect.any(Number) },
      { target: 'sealed', rating: expect.any(Number) },
      { target: 'theatre', rating: expect.any(Number) }
    ]);
  });

  test('returns the bestMatch object with the highest rating', () => {
    const result = findBestMatch('healed', ['edward', 'sealed', 'theatre']);
    expect(result.bestMatch).toHaveProperty('target', 'sealed');
  });

  test('returns the bestMatchIndex corresponding to the best match', () => {
    const result = findBestMatch('healed', ['edward', 'sealed', 'theatre']);
    expect(result.bestMatchIndex).toBe(1);
  });
});