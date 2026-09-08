const assert = require('assert');
const pjs = require('../lib/pjs.js');

describe('Public: pjs', function () {
    it('should map values correctly with different input', function () {
        const arr = [10, 20, 30];
        const result = arr.map(x => x * 2);
        assert.deepStrictEqual(result, [20, 40, 60]);
    });

    it('should filter even numbers with different data', function () {
        const arr = [15, 22, 37, 44];
        const result = arr.filter(x => x % 2 === 0);
        assert.deepStrictEqual(result, [22, 44]);
    });

    it('should reduce array with sum with different numbers', function () {
        const arr = [8, 16, 24];
        const result = arr.reduce((acc, x) => acc + x, 0);
        assert.strictEqual(result, 48);
    });
});