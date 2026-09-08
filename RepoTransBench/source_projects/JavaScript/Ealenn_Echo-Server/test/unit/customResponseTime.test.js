const assert = require('assert');

describe('customResponseTime', function () {
  it('should be a function', function () {
    const customResponseTime = require('../../src/middlewares/customResponseTime.js');
    assert.equal(typeof customResponseTime, 'function');
  });
});