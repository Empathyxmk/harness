const assert = require('assert');
const fuge = require('../fuge');

describe('basic fuge public API (public)', function () {
  it('should have property that is a function (different name)', function () {
    // The export may change - so test for any function property not just one named 'run'
    const keys = Object.keys(fuge);
    assert(keys.find(key => typeof fuge[key] === 'function'), 'should have at least one function property');
  });
});