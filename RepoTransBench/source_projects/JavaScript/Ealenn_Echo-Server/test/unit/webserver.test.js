const assert = require('assert');

describe('webserver', function () {
  it('should export something', function () {
    const webserver = require('../../src/webserver.js');
    assert.ok(webserver);
  });
});