/**
 * Public test for ch05 concepts with new data
 */

describe('Chapter 5 (public)', () => {
  test('should simulate monadic composition with numbers', () => {
    const add2 = x => x + 2;
    const square = x => x * x;
    const compose = (f, g) => x => f(g(x));
    const result = compose(square, add2)(6); // (6 + 2)^2 = 64
    expect(result).toBe(64);
  });

  test('should chain mapped effects for string transformations', () => {
    const shout = s => s + '!';
    const toUpper = s => s.toUpperCase();
    const trim = s => s.trim();
    const chain = (f, g) => x => g(f(x));
    expect(chain(trim, toUpper)('  hiya ')).toBe('HIYA');
    expect(chain(toUpper, shout)('amazing')).toBe('AMAZING!');
  });
});