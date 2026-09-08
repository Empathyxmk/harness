// Public proxy test for index.js with different require flows (data not the same as existing)
const assert = require('assert');

describe('index.js (public)', function() {
  it('should export and resolve lib/index.js (public)', function() {
    // Slightly different require chain: 
    // make sure exported module matches expected by type
    const lib = require('../lib/index.js');
    const packageMain = require('../index.js');
    assert.strictEqual(typeof packageMain, typeof lib);
    // (public) - this is essentially a proxy, so we could test a property
    assert.ok(lib && typeof lib === 'object');
  });
});