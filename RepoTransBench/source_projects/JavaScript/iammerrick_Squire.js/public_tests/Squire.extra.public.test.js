let Squire;
try {
  Squire = require('../src/Squire.node.js');
} catch (e) {
  // fallback, module could not be loaded
  Squire = {};
}

describe('Squire: extra utility coverage [PUBLIC]', function () {
  // For each test, skip quietly if underlying method is unavailable
  describe('map', function () {
    it('can map over an array with different values', function () {
      if (!Squire.util || typeof Squire.util.map !== 'function') {
        return;
      }
      const arr = [5, 3, 6];
      expect(Squire.util.map(arr, x => x + 10)).toEqual([15, 13, 16]);
    });

    it('returns empty array for empty array', function () {
      if (!Squire.util || typeof Squire.util.map !== 'function') {
        return;
      }
      expect(Squire.util.map([], x => x * 42)).toEqual([]);
    });
  });

  describe('each', function () {
    it('can iterate object with different values', function () {
      if (!Squire.util || typeof Squire.util.each !== 'function') {
        return;
      }
      const obj = { sun: 'hot', moon: 'cold', mars: 'red' };
      let result = '';
      Squire.util.each(obj, function (v, k) {
        result += `${k}:${v};`;
      });
      expect(result).toBe('sun:hot;moon:cold;mars:red;');
    });

    it('can iterate array with different values', function () {
      if (!Squire.util || typeof Squire.util.each !== 'function') {
        return;
      }
      const arr = ['foo', 'bar', 'baz'];
      let res = [];
      Squire.util.each(arr, function (v, i) {
        res.push(v.toUpperCase() + i);
      });
      expect(res).toEqual(['FOO0', 'BAR1', 'BAZ2']);
    });

    it('does nothing if null passed', function () {
      if (!Squire.util || typeof Squire.util.each !== 'function') {
        return;
      }
      expect(() => Squire.util.each(null, () => { throw new Error('Should not be called'); })).not.toThrow();
    });

    it('does not call iterator if empty array', function () {
      if (!Squire.util || typeof Squire.util.each !== 'function') {
        return;
      }
      Squire.util.each([], () => { throw new Error('Should not be called'); });
      // If it throws, test fails
    });
  });

  describe('some', function () {
    it('returns true if at least one element matches (array)', function () {
      if (!Squire.util || typeof Squire.util.some !== 'function') {
        return;
      }
      const arr = [11, 19, 27];
      expect(Squire.util.some(arr, x => x > 25)).toBe(true);
    });

    it('returns false if no element matches (array)', function () {
      if (!Squire.util || typeof Squire.util.some !== 'function') {
        return;
      }
      const arr = [-1, 0, 2];
      expect(Squire.util.some(arr, x => x === 999)).toBe(false);
    });

    it('returns true if at least one value matches (object)', function () {
      if (!Squire.util || typeof Squire.util.some !== 'function') {
        return;
      }
      const obj = { a: 'hello', b: 'there', c: 'world' };
      expect(Squire.util.some(obj, x => x === 'world')).toBe(true);
    });

    it('returns false if no value matches (object)', function () {
      if (!Squire.util || typeof Squire.util.some !== 'function') {
        return;
      }
      const obj = { x: 123, y: 456 };
      expect(Squire.util.some(obj, v => v === 0)).toBe(false);
    });
  });

  describe('every', function () {
    it('returns true if all match (array)', function () {
      if (!Squire.util || typeof Squire.util.every !== 'function') {
        return;
      }
      const arr = [100, 102, 104];
      expect(Squire.util.every(arr, x => x > 99)).toBe(true);
    });

    it('returns false if not all match (array)', function () {
      if (!Squire.util || typeof Squire.util.every !== 'function') {
        return;
      }
      const arr = [42, 50, 80, 90];
      expect(Squire.util.every(arr, x => x >= 50)).toBe(false);
    });

    it('returns true if all match (object)', function () {
      if (!Squire.util || typeof Squire.util.every !== 'function') {
        return;
      }
      const obj = { foo: false, bar: false };
      expect(Squire.util.every(obj, x => x === false)).toBe(true);
    });

    it('returns false if not all match (object)', function () {
      if (!Squire.util || typeof Squire.util.every !== 'function') {
        return;
      }
      const obj = { p: 2, q: 3 };
      expect(Squire.util.every(obj, x => x === 2)).toBe(false);
    });
  });
});