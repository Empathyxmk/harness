const donut = require('../../src/modules/donut/donut.js');

describe('donut.js isDonut (public)', () => {
  it('should return true for "Donut" (case sensitive check)', () => {
    expect(donut.isDonut('Donut')).toBe(false); // Check it doesn't accidentally work with capital D
  });
  it('should return false for unrelated shapes', () => {
    expect(donut.isDonut('ring')).toBe(false);
    expect(donut.isDonut(null)).toBe(false);
  });
});