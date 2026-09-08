/**
 * Public test for ch08 with new data
 */
describe('Chapter 8 public', () => {
  test('should filter strings whose length > 5', () => {
    const arr = ['pear', 'banana', 'plum', 'coconut', 'fig'];
    const result = arr.filter(x => x.length > 5);
    expect(result).toEqual(['banana', 'coconut']);
  });

  test('should find index of a different element in array', () => {
    const arr = ['red', 'blue', 'green', 'yellow'];
    expect(arr.indexOf('green')).toBe(2);
  });
});