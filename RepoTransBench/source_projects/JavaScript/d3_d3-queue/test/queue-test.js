// Patch: use queue.cjs
const assert = require('assert');
const queue = require('../src/queue.cjs');

describe('Queue', function() {
  it('should process tasks in series by default', function(done) {
    let order = [];
    let q = queue.queue();
    q.defer(cb => { setTimeout(() => {order.push(1); cb(null, 1);}, 10); });
    q.defer(cb => { setTimeout(() => {order.push(2); cb(null, 2);}, 5); });
    q.awaitAll(function(err, results) {
      assert.strictEqual(err, null);
      assert.deepStrictEqual(results, [1,2]);
      assert.deepStrictEqual(order, [1,2]);
      done();
    });
  });

  it('should handle multiple concurrency', function(done) {
    let order = [];
    let q = queue.queue(2);
    q.defer(cb => { setTimeout(() => {order.push(1); cb(null, 1);}, 10); });
    q.defer(cb => { setTimeout(() => {order.push(2); cb(null, 2);}, 5); });
    q.awaitAll(function(err, results) {
      assert.strictEqual(err, null);
      assert.deepStrictEqual(results.sort(), [1,2]);
      done();
    });
  });

  it('should throw when defer called after awaitAll', function() {
    let q = queue.queue();
    q.awaitAll(()=>{});
    assert.throws(() => q.defer(()=>{}), /defer after await/);
  });

  it('should throw when awaitAll called twice', function() {
    let q = queue.queue();
    q.defer(cb => cb(null, 1));
    q.awaitAll(()=>{});
    assert.throws(() => q.awaitAll(()=>{}), /multiple await/);
  });

  it('should propagate thrown errors', function(done) {
    let q = queue.queue();
    q.defer(() => { throw new Error('fail!'); });
    q.awaitAll(function(err) {
      assert.ok(err instanceof Error);
      assert.strictEqual(err.message, 'fail!');
      done();
    });
  });

  it('should error if .defer is not a function', function() {
    let q = queue.queue();
    assert.throws(() => q.defer(42), /callback is not a function/);
  });
});