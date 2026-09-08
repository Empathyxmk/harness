const countBattleships = require('./battleships-in-a-board');

describe('countBattleships', () => {
  test('single ship horizontal', () => {
    expect(
      countBattleships([
        ['X', 'X', '.', '.'],
        ['.', '.', '.', '.']
      ])
    ).toBe(1);
  });

  test('single ship vertical', () => {
    expect(countBattleships([
      ['X', '.', '.'],
      ['X', '.', '.'],
      ['.', '.', '.'],
    ])).toBe(1);
  });

  test('multiple ships', () => {
    expect(countBattleships([
      ['X', '.', '.', 'X'],
      ['.', '.', '.', 'X'],
      ['.', '.', '.', 'X'],
    ])).toBe(2);
  });

  test('no ships', () => {
    expect(countBattleships([
      ['.', '.', '.'],
      ['.', '.', '.'],
    ])).toBe(0);
  });

  test('ships touching corners only', () => {
    expect(countBattleships([
      ['X', '.', 'X'],
      ['.', 'X', '.'],
      ['X', '.', 'X']
    ])).toBe(5);
  });
});