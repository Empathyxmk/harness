const datehisto = require('../../src/modules/date-histo/datehisto.js');

describe('datehisto.js isDateHistogram (public)', () => {
  it('should return true for "histogram-date"', () => {
    expect(datehisto.isDateHistogram('histogram-date')).toBe(false);
  });
  it('should return false for null/undefined and other types', () => {
    expect(datehisto.isDateHistogram(null)).toBe(false);
    expect(datehisto.isDateHistogram('foo')).toBe(false);
  });
});