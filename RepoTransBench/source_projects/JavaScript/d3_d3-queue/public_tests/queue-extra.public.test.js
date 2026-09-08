const assert = require('assert');
const queue = require('../src/queue.cjs');

describe('Queue - extra cases (public)', function() {
  it('should not start tasks above concurrency (public, different times/data)', function(done) {
    let started = 0;
    let q = queue.queue(2); // concurrency = 2

    q.defer(cb => { started++; setTimeout(() => cb(null, 100), 12); });
    q.defer(cb => { started++; setTimeout(() => cb(null, 200), 8); });
    q.defer(cb => { started++; setTimeout(() => cb(null, 300), 5); });
    q.awaitAll(function(err, results) {
      assert.strictEqual(started, 3);
      assert.strictEqual(err, null);
      assert.deepStrictEqual(results, [100, 200, 300]);
      done();
    });
  });

  it('should propagate errors and abort remaining tasks (different error/data)', function(done) {
    let called = false;
    let q = queue.queue(2);
    q.defer(cb => cb(new Error('public expected')));
    q.defer(cb => { called = true; cb(null, 55); }); // Should never run
    q.awaitAll(function(err, results) {
      assert.ok(err instanceof Error);
      assert.strictEqual(err.message, 'public expected');
      assert.strictEqual(called, false);
      done();
    });
  });
});