const Squire = require('../src/Squire.node.js');

describe('Squire.js Utility Functions [PUBLIC]', () => {
  describe('isArray', () => {
    it('returns true for arrays (different values)', () => {
      expect(Squire.isArray(['a', 'b', 'c'])).toBe(true);
      expect(Squire.isArray(new Array(2))).toBe(true);
    });
    it('returns false for other types (different values)', () => {
      expect(Squire.isArray({ foo: 'bar' })).toBe(false);
      expect(Squire.isArray(123)).toBe(false);
      expect(Squire.isArray('not-array')).toBe(false);
      expect(Squire.isArray(false)).toBe(false);
    });
  });

  describe('isFunction', () => {
    it('returns true for regular and arrow functions (diff)', () => {
      function testFunc() {}
      const arrowFunc = v => v * 2;
      expect(Squire.isFunction(testFunc)).toBe(true);
      expect(Squire.isFunction(arrowFunc)).toBe(true);
    });
    it('returns false for many non-functions', () => {
      expect(Squire.isFunction([1, 2, 3])).toBe(false);
      expect(Squire.isFunction('function')).toBe(false);
      expect(Squire.isFunction(0)).toBe(false);
      expect(Squire.isFunction(undefined)).toBe(false);
    });
  });

  describe('indexOf', () => {
    it('returns index of found value (different array/data)', () => {
      expect(Squire.indexOf(['x', 'y', 'z'], 'z')).toBe(2);
    });
    it('returns -1 if not found, empty/different data', () => {
      expect(Squire.indexOf(['a', 'b'], 'c')).toBe(-1);
      expect(Squire.indexOf([], 99)).toBe(-1);
    });
    it('finds objects by reference in different array', () => {
      const obj2 = { test: true };
      const arr2 = [{}, obj2, 7];
      expect(Squire.indexOf(arr2, obj2)).toBe(1);
    });
  });
});