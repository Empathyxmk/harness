const proxyquire = require('proxyquire');
const assert = require('assert');

describe('Public App', function () {
  it('should not throw when loading with custom stubs', function () {
    let app;
    // Use a different approach: stub out './nconf' with a dummy object, still expect it not to throw
    assert.doesNotThrow(() => {
      app = proxyquire('../../src/app.js', {
        './nconf': { get: () => 1234 }
      });
    });
    assert.ok(app);
  });
});