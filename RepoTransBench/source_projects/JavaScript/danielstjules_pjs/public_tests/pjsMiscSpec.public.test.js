const assert = require('assert');
const pjs = require('../lib/pjs.js');

describe('Public: pjs Misc', function () {
    it('should join array elements with custom separator', function () {
        const arr = ['cat', 'dog', 'bird'];
        assert.strictEqual(arr.join(' | '), 'cat | dog | bird');
    });
    it('should reverse an array with different values', function () {
        const arr = [4, 5, 6, 7];
        assert.deepStrictEqual(arr.reverse(), [7, 6, 5, 4]);
    });
});