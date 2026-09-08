// Test for index.js, just validates the proxy re-export works
const assert = require('assert');

describe('Project entry index.js', () => {
  it('should proxy require ./lib', () => {
    const top = require('../index');
    const lib = require('../lib');
    assert.deepStrictEqual(
      Object.keys(top).sort(),
      Object.keys(lib).sort()
    );
  });
});