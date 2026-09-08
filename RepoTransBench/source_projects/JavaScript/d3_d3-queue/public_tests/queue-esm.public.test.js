const assert = require('assert');
// queue.js is ES Module, but the default build exports through queue.cjs for Node test convenience
const queue = require('../src/queue.cjs');

describe('Queue ESM - public', function() {
  it('queue() should accept different concurrency number (public)', function(done) {
    const q = queue.queue(4);
    let result = [];
    for (let i=0; i<4; ++i) {
      q.defer(cb => setTimeout(() => { result[i]=i+1; cb(null, i+1); }, 3*(i+1)));
    }
    q.awaitAll(function(err, results) {
      assert.strictEqual(err, null);
      assert.deepStrictEqual(results, [1,2,3,4]);
      done();
    });
  });

  it('queue().defer should support argument passing (different data/args)', function(done) {
    const q = queue.queue();
    function add(a, b, cb) {
      setTimeout(() => cb(null, a * b), 2);
    }
    q.defer(add, 7, 3);
    q.defer(add, 2, 6);
    q.awaitAll(function(err, results) {
      assert.strictEqual(err, null);
      assert.deepStrictEqual(results, [21, 12]);
      done();
    });
  });
});