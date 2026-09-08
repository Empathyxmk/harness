const findComplement = require('./number-complement');

describe('findComplement', () => {
  test('returns complement of a positive number', () => {
    expect(findComplement(5)).toBe(2); // 101 -> 010
    expect(findComplement(1)).toBe(0); // 1 -> 0
    expect(findComplement(8)).toBe(7); // 1000 -> 0111
    expect(findComplement(0)).toBe(1); // 0 -> ?
  });

  test('returns 0 for 0', () => {
    expect(findComplement(0)).toBe(1);
  });
});