const assert = require('assert');

describe('Public: utils', function () {
    it('should check if all elements in array are positive', function () {
        const arr = [2, 4, 6, 8];
        assert.strictEqual(arr.every(x => x > 0), true);
    });
    it('should find element greater than specific value', function () {
        const arr = [12, 28, 19, 31];
        assert.strictEqual(arr.find(x => x > 20), 28);
    });
});