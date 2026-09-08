const proxyquire = require('proxyquire');
const assert = require('assert');

describe('App', function () {
  it('should load without throwing', function () {
    let app;
    assert.doesNotThrow(() => {
      app = proxyquire('../../src/app.js', {});
    });
    assert.ok(app);
  });
});