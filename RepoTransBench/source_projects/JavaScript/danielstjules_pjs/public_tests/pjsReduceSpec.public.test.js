const assert = require('assert');
const pjs = require('../lib/pjs.js');

describe('Public: pjs Reduce', function () {
    it('should multiply array elements via reduce', function () {
        const arr = [2, 3, 4];
        const result = arr.reduce((acc, x) => acc * x, 1);
        assert.strictEqual(result, 24);
    });
    it('should find minimum of array', function () {
        const arr = [11, 3, 7, 2];
        const result = arr.reduce((min, x) => Math.min(min, x), arr[0]);
        assert.strictEqual(result, 2);
    });
});