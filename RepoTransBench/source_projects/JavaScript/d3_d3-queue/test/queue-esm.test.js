// Test coverage for src/queue.js (ESM)
// NOTE: This requires an ESM importer; for coverage it's valuable to directly test the default export

const assert = require('assert');

let queueESM;
before(async function() {
  queueESM = (await import('../src/queue.js')).default;
});

describe('Queue ESM', function() {
  it('throws if concurrency < 1', function() {
    assert.throws(() => queueESM(0), /invalid concurrency/);
    assert.throws(() => queueESM(-5), /invalid concurrency/);
  });

  it('defaults concurrency to Infinity', function() {
    const q = queueESM();
    assert.strictEqual(q._size, Infinity);
  });

  it('throws if .defer argument is not a function', function() {
    const q = queueESM(2);
    assert.throws(() => q.defer(123), /invalid callback/);
    assert.throws(() => q.defer(null), /invalid callback/);
  });

  it('throws if .await called with non-function', function() {
    const q = queueESM(2);
    assert.throws(() => q.await(123), /invalid callback/);
  });

  it('throws if .awaitAll called with non-function', function() {
    const q = queueESM(2);
    assert.throws(() => q.awaitAll(123), /invalid callback/);
  });

  it('throws if .await called twice', function() {
    const q = queueESM(2);
    q.await(() => {});
    assert.throws(() => q.await(() => {}), /multiple await/);
  });

  it('throws if .defer after .await called', function() {
    const q = queueESM(2);
    q.await(() => {});
    assert.throws(() => q.defer(() => {}), /defer after await/);
  });

  it('processes a basic asynchronous callback task', function(done) {
    const q = queueESM(2);
    q.defer((cb) => setTimeout(() => cb(null, 5), 3));
    q.await(function(err, a, b) {
      assert.strictEqual(err, null);
      assert.strictEqual(a, 5);
      done();
    });
  });

  it('handles queue.abort()', function(done) {
    const q = queueESM(1);
    let cbCalled = false;
    q.defer(cb => setTimeout(() => cb(null, 7), 5));
    q.await((err, res) => {
      cbCalled = true;
      assert(err instanceof Error);
      assert.strictEqual(err.message, "abort");
      done();
    });
    q.abort();
  });
});