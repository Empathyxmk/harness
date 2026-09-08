/**
 * Public test for ch06/jscheck - property-based, public values
 */

describe('Chapter 6 jscheck public', () => {
  test('should always produce even product for paired evens', () => {
    const isEven = n => n % 2 === 0;
    for (let a = 2; a <= 10; a += 2) {
      for (let b = 2; b <= 10; b += 2) {
        expect(isEven(a * b)).toBe(true);
      }
    }
  });

  test('should fail to find 13 in a small odd array', () => {
    const arr = [1, 3, 5, 7, 9, 11];
    expect(arr.includes(13)).toBe(false);
  });
});