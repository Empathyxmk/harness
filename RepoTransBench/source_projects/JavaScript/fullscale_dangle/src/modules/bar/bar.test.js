const bar = require('./bar.js');

describe('bar.js add', () => {
  it('should add two numbers', () => {
    expect(bar.add(2, 3)).toBe(5);
  });
  it('should return 0 for defaults', () => {
    expect(bar.add()).toBe(0);
  });
  it('should throw for NaN', () => {
    expect(() => bar.add(NaN, 2)).toThrow('Invalid number');
    expect(() => bar.add(2, NaN)).toThrow('Invalid number');
  });
});