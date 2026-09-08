const column = require('./column.js');

describe('column.js stringToUpper', () => {
  it('should convert string to uppercase', () => {
    expect(column.stringToUpper('foo')).toBe('FOO');
  });
  it('should return empty string on falsy input', () => {
    expect(column.stringToUpper('')).toBe('');
    expect(column.stringToUpper(null)).toBe('');
    expect(column.stringToUpper(undefined)).toBe('');
  });
});