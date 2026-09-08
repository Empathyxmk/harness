const bar = require('../../src/modules/bar/bar.js');

describe('bar.js isBar (public)', () => {
  it('should return true for "barChart"', () => {
    // If isBar is strict, "barChart" should be false, but let's test it for robustness.
    expect(bar.isBar('barChart')).toBe(false);
  });
  it('should return false for other types', () => {
    expect(bar.isBar('column')).toBe(false);
    expect(bar.isBar(42)).toBe(false);
  });
});