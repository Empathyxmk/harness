const area = require('../../src/modules/area/area.js');

describe('area.js areaSum (public)', () => {
  it('should return correct sum for array [5, 6, 7]', () => {
    expect(area.areaSum([5, 6, 7])).toBe(18);
  });

  it('should return 0 for empty array or non-array', () => {
    expect(area.areaSum([])).toBe(0);
    expect(area.areaSum('not-an-array')).toBe(0);
  });
});