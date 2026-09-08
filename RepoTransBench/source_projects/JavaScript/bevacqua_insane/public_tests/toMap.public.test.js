const toMap = require('../toMap');

describe('toMap (public)', () => {
  it('should turn array of numbers (as strings) into key-object', () => {
    const arr = ['42', '88', '100'];
    expect(toMap(arr)).toEqual({ '42': true, '88': true, '100': true });
  });

  it('should handle empty array', () => {
    expect(toMap([])).toEqual({});
  });

  it('should work with array of booleans as strings', () => {
    const arr = ['true', 'false', 'TRUE'];
    expect(toMap(arr)).toEqual({ 'true': true, 'false': true, 'TRUE': true });
  });
});