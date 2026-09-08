test('parseInt on hexadecimal string (public)', () => {
  expect(parseInt('2A', 16)).toBe(42);
});
test('parseFloat with leading/trailing whitespace (public)', () => {
  expect(parseFloat('   9.81  ')).toBeCloseTo(9.81, 2);
});
test('parseInt returns NaN for non-parsable input (public)', () => {
  expect(isNaN(parseInt('duck', 10))).toBe(true);
});