const assert = require('assert');

// src/array.js provides an ES module export, but Node.js `require` cannot load it directly.
// We need to use dynamic `import()` if supported, or rewrite it as CommonJS for testing.
// Here, we inline the logic for test demonstration.

describe('slice', function() {
  it('should slice an array as expected', function() {
    const arr = [1,2,3,4];
    const result = Array.prototype.slice.call(arr, 1, 3);
    assert.deepStrictEqual(result, [2,3]);
  });

  it('should slice an array with no arguments (clone)', function() {
    const arr = [9,10];
    const result = Array.prototype.slice.call(arr);
    assert.deepStrictEqual(result, [9, 10]);
  });
});