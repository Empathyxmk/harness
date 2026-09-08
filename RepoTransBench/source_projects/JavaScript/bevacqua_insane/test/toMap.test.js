const toMap = require('../toMap');

describe('toMap', () => {
  it('should convert an array to a map', () => {
    expect(toMap(['a', 'b', 'c'])).toEqual({ a: true, b: true, c: true });
  });

  it('should return empty object for an empty array', () => {
    expect(toMap([])).toEqual({});
  });

  it('should handle duplicate values in array', () => {
    expect(toMap(['a', 'a', 'b'])).toEqual({ a: true, b: true });
  });
});