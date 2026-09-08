const stringSimilarity = require('../src/index');
const findBestMatch = stringSimilarity.findBestMatch;

describe('findBestMatch (public tests)', () => {
  const badArgsErrorMsg = 'Bad arguments: First argument should be a string, second should be an array of strings';

  test("throws a 'Bad arguments' error if no arguments passed", () => {
    expect(() => findBestMatch()).toThrow(badArgsErrorMsg);
  });

  test("throws a 'Bad arguments' error if first argument is not a string", () => {
    expect(() => findBestMatch(true)).toThrow(badArgsErrorMsg);
    expect(() => findBestMatch([])).toThrow(badArgsErrorMsg);
  });

  test("throws a 'Bad arguments' error if second argument is not an array", () => {
    expect(() => findBestMatch('sample', 'item')).toThrow(badArgsErrorMsg);
    expect(() => findBestMatch('sample', 123)).toThrow(badArgsErrorMsg);
  });

  test("throws a 'Bad arguments' error if second argument is not an array of strings", () => {
    expect(() => findBestMatch('sample', [{}, 'item'])).toThrow(badArgsErrorMsg);
  });

  test('assigns a similarity rating to each string passed in the array', () => {
    const result = findBestMatch('marker', ['baker', 'maker', 'faker']);
    expect(result.ratings).toEqual([
      { target: 'baker', rating: expect.any(Number) },
      { target: 'maker', rating: expect.any(Number) },
      { target: 'faker', rating: expect.any(Number) }
    ]);
  });

  test('returns the bestMatch object with the highest rating', () => {
    const result = findBestMatch('marker', ['baker', 'maker', 'faker']);
    expect(result.bestMatch).toHaveProperty('target', 'maker');
  });

  test('returns the bestMatchIndex corresponding to the best match', () => {
    const result = findBestMatch('marker', ['baker', 'maker', 'faker']);
    expect(result.bestMatchIndex).toBe(1);
  });
});