const assert = require('assert');
const proxyquire = require('proxyquire');

describe('Public customResponseTime middleware', function () {
  it('should export as a function and not throw when executed', function () {
    // Instead of direct require like existing test, use proxyquire to inject a dummy dependency if needed;
    // also, test execution as a function (call it with dummy arguments)
    const middleware = proxyquire('../../src/middlewares/customResponseTime', {});
    assert.strictEqual(typeof middleware, 'function');

    let calledNext = false;
    const ctx = {};
    const next = () => { calledNext = true; };
    middleware(ctx, next);
    assert.ok(calledNext, "next() should be called");
  });
});