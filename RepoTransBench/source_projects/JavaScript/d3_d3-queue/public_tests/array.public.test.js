const assert = require('assert');

describe('slice - public', function() {
  it('should slice an array as expected (different indices)', function() {
    const arr = [5,6,7,8,9];
    const result = Array.prototype.slice.call(arr, 2, 4);
    assert.deepStrictEqual(result, [7,8]);
  });

  it('should slice an array with no arguments (clone, different array)', function() {
    const arr = [21, 42];
    const result = Array.prototype.slice.call(arr);
    assert.deepStrictEqual(result, [21, 42]);
  });
});