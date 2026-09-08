/**
 * Public test for ch06 chapter - different functional input
 */

describe('Chapter 6 public', () => {
  test('should filter odds and sum from new set', () => {
    const arr = [7, 4, 9, 12];
    const sumOdds = arr => arr.filter(x => x % 2 !== 0).reduce((a, b) => a + b, 0);
    expect(sumOdds(arr)).toBe(16); // 7+9
  });

  test('should map new objects to ids', () => {
    const data = [{ id: 'x' }, { id: 'y' }, { id: 'z' }];
    expect(data.map(obj => obj.id)).toEqual(['x', 'y', 'z']);
  });
});