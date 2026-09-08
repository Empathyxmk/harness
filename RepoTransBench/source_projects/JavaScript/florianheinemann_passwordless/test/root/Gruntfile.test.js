const assert = require('assert');
const path = require('path');

describe('Gruntfile.js', () => {
  it('should be loadable as a function', () => {
    const gruntfilePath = path.resolve(__dirname, '../../Gruntfile.js');
    const gruntfile = require(gruntfilePath);
    assert.strictEqual(typeof gruntfile, 'function');
  });
});