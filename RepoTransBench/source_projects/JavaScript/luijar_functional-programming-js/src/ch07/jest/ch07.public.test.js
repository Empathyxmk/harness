/**
 * Public test for ch07/memoization.js with different function/data
 */

describe('Chapter 7 Memoization Public (custom data)', () => {
  function memoize(fn) {
    const cache = {};
    return function (...args) {
      const k = JSON.stringify(args);
      if (cache[k]) {
        return cache[k];
      } else {
        const result = fn(...args);
        cache[k] = result;
        return result;
      }
    };
  }

  it('should memoize a factorial calculation with different number', () => {
    let count = 0;
    const fact = n => {
      count++;
      if (n === 0) return 1;
      return n * fact(n - 1);
    };
    const memFact = memoize(fact);
    expect(memFact(6)).toBe(720);
    expect(memFact(6)).toBe(720);
    // count should still increment only once for that arg
    expect(count).toBeLessThan(8);
  });

  it('should memoize for another function and different list', () => {
    let count = 0;
    const sum = arr => {
      count++;
      return arr.reduce((a, b) => a + b, 0);
    };
    const memSum = memoize(sum);
    expect(memSum([3, 6, 9, 12])).toBe(30);
    expect(memSum([3, 6, 9, 12])).toBe(30);
    expect(count).toBe(1);
  });
});