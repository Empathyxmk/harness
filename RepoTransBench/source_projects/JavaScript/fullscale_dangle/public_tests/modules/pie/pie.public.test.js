const pie = require('../../src/modules/pie/pie.js');

describe('pie.js slices (public)', () => {
  it('should return array of slices for another positive n', () => {
    expect(pie.slices(5)).toEqual([1, 2, 3, 4, 5]);
  });
  it('should return empty array for n < 1 (different values)', () => {
    expect(pie.slices(-2)).toEqual([]);
    expect(pie.slices(0)).toEqual([]);
  });
  it('should return empty array for non-number (additional values)', () => {
    expect(pie.slices({})).toEqual([]);
    expect(pie.slices([])).toEqual([]);
  });
});