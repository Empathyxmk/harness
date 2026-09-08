const donut = require('./donut.js');

describe('donut.js isDonut', () => {
  it('should return true for "donut"', () => {
    expect(donut.isDonut('donut')).toBe(true);
  });
  it('should return false for other shapes', () => {
    expect(donut.isDonut('pie')).toBe(false);
    expect(donut.isDonut(undefined)).toBe(false);
  });
});