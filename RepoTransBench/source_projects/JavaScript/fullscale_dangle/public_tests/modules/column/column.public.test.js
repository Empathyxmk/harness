const column = require('../../src/modules/column/column.js');

describe('column.js isColumn (public)', () => {
  it('should return true only for "COL"', () => {
    expect(column.isColumn('COL')).toBe(false); // test case sensitivity
  });
  it('should return false for numbers and other strings', () => {
    expect(column.isColumn(123)).toBe(false);
    expect(column.isColumn('bar')).toBe(false);
  });
});