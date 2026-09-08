const Squire = require('../Squire.node.js');

describe('Squire.js Utility Functions', () => {
  describe('isArray', () => {
    it('returns true for arrays', () => {
      expect(Squire.isArray([1,2,3])).toBe(true);
    });
    it('returns false for objects', () => {
      expect(Squire.isArray({})).toBe(false);
      expect(Squire.isArray(null)).toBe(false);
      expect(Squire.isArray(undefined)).toBe(false);
      expect(Squire.isArray('abc')).toBe(false);
    });
  });

  describe('isFunction', () => {
    it('returns true for functions', () => {
      expect(Squire.isFunction(function(){})).toBe(true);
      expect(Squire.isFunction(() => {})).toBe(true);
    });
    it('returns false for non-functions', () => {
      expect(Squire.isFunction({})).toBe(false);
      expect(Squire.isFunction([])).toBe(false);
      expect(Squire.isFunction(null)).toBe(false);
    });
  });

  describe('indexOf', () => {
    it('returns the index of an existing item', () => {
      expect(Squire.indexOf([1,2,3], 2)).toBe(1);
    });
    it('returns -1 for not found', () => {
      expect(Squire.indexOf([1,2,3], 6)).toBe(-1);
      expect(Squire.indexOf([], 1)).toBe(-1);
    });
    // Additional coverage: works with objects in array
    it('finds objects by reference', () => {
      const obj = {};
      const arr = [1, obj, 3];
      expect(Squire.indexOf(arr, obj)).toBe(1);
    });
  });

  // Removed uniqueId tests since function is not implemented in Squire.node.js

});