const countBattleships = require('./battleships-in-a-board');

describe('countBattleships (public)', () => {
  test('1x1 board with X', () => {
    expect(countBattleships([['X']])).toBe(1);
  });

  test('1x2 vertical ship', () => {
    expect(countBattleships([['X'],['X']])).toBe(1);
  });

  test('2x2, two ships placed diagonally', () => {
    expect(countBattleships([
      ['X','.'],
      ['.','X']
    ])).toBe(2);
  });

  test('vertical ship and another separate ship', () => {
    expect(countBattleships([
      ['X','.','.'],
      ['X','.','X'],
      ['.','.','X']
    ])).toBe(2);
  });

  test('bigger board, ships in odd positions', () => {
    expect(countBattleships([
      ['.', 'X', '.', '.', 'X'],
      ['.', '.', '.', 'X', '.'],
      ['X', '.', '.', '.', '.'],
      ['.', '.', 'X', '.', '.']
    ])).toBe(5);
  });

  test('single row, max ships', () => {
    expect(countBattleships([['X','.','X','X','.','X']])).toBe(3);
  });

  test('all water', () => {
    expect(countBattleships([
      ['.','.'],
      ['.','.']
    ])).toBe(0);
  });

  // Corrected input so number of true battleships matches expected output (7 ships).
  test('many ships separated', () => {
    expect(countBattleships([
      ['X', '.', '.', 'X', '.'],
      ['.', 'X', '.', 'X', '.'],
      ['.', '.', 'X', '.', '.'],
      ['.', '.', '.', 'X', '.'],
      ['X', '.', '.', '.', 'X']
    ])).toBe(7);
  });
});