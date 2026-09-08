const pie = require('./pie.js');

describe('pie.js slices', () => {
  it('should return array of slices for positive n', () => {
    expect(pie.slices(3)).toEqual([1, 2, 3]);
  });
  it('should return empty array for n < 1', () => {
    expect(pie.slices(0)).toEqual([]);
    expect(pie.slices(-1)).toEqual([]);
  });
  it('should return empty array for non-number', () => {
    expect(pie.slices('foo')).toEqual([]);
    expect(pie.slices()).toEqual([]);
  });
});