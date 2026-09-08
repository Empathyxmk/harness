const findComplement = require('./number-complement');

describe('findComplement (public)', () => {
  test('returns complement of another positive number', () => {
    expect(findComplement(10)).toBe(5); // 1010 -> 0101
    expect(findComplement(6)).toBe(1);  // 110 -> 001
    expect(findComplement(15)).toBe(0); // 1111 -> 0000
    expect(findComplement(9)).toBe(6);  // 1001 -> 0110
  });

  test('edge cases (still expect 1 for 0)', () => {
    expect(findComplement(0)).toBe(1);
  });
});