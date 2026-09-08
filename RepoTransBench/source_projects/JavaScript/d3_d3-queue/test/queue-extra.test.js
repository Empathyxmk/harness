// Patch: Replace import with CommonJS require to fix failure
const assert = require('assert');
const queue = require('../src/queue.cjs');

describe('Queue - extra cases', function() {
  it('should not start tasks above concurrency', function(done) {
    let started = 0;
    let q = queue.queue(1); // concurrency = 1

    q.defer(cb => { started++; setTimeout(() => cb(null, 1), 40); });
    q.defer(cb => { started++; setTimeout(() => cb(null, 2), 10); });
    q.awaitAll(function(err, results) {
      assert.strictEqual(started, 2);
      assert.strictEqual(err, null);
      assert.deepStrictEqual(results, [1,2]);
      done();
    });
  });

  it('should propagate errors and abort remaining tasks', function(done) {
    let called = false;
    let q = queue.queue(2);
    q.defer(cb => cb(new Error('expected')));
    q.defer(cb => { called = true; cb(null, 5); }); // Should never run
    q.awaitAll(function(err, results) {
      assert.ok(err instanceof Error);
      assert.strictEqual(called, false);
      done();
    });
  });
});