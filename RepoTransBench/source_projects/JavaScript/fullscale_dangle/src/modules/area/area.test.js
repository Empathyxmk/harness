const area = require('./area.js');

describe('area.js exampleMethodArea', () => {
  it('should return "a" when a > b', () => {
    expect(area.exampleMethodArea(3, 1)).toBe('a');
  });
  it('should return "b" when a < b', () => {
    expect(area.exampleMethodArea(1, 3)).toBe('b');
  });
  it('should return "equal" when a === b', () => {
    expect(area.exampleMethodArea(2, 2)).toBe('equal');
  });
  it('should return "equal" for defaults', () => {
    expect(area.exampleMethodArea()).toBe('equal');
  });
});