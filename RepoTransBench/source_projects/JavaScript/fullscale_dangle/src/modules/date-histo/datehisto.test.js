const datehisto = require('./datehisto.js');

describe('datehisto.js formatDate', () => {
  it('should return ISO date string for valid input', () => {
    expect(datehisto.formatDate('2024-01-01T00:00:00Z')).toBe('2024-01-01');
  });
  it('should return empty string for undefined', () => {
    expect(datehisto.formatDate()).toBe('');
  });
  it('should return "Invalid" for invalid date', () => {
    expect(datehisto.formatDate('foo')).toBe('Invalid');
  });
});