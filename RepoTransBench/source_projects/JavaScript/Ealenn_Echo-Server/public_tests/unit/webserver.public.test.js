const assert = require('assert');

describe('Public webserver', function () {
  it('should have a listen property or method', function () {
    const webserver = require('../../src/webserver.js');
    // slightly different: check if webserver has a property like listen (should be app)
    assert.ok(webserver && (typeof webserver.listen === "function" || 'use' in webserver));
  });
});