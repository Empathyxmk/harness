const assert = require('assert');
const queue = require('../src/queue.cjs');

// Helper to create an async task
function makeTask(value, error) {
  return function(cb) {
    setTimeout(() => {
      if (error) cb(error);
      else cb(null, value);
    }, 1);
  };
}

describe('Queue CJS Extra', function() {

  it('throws if defer argument is not a function', function() {
    const q = queue.queue();
    assert.throws(() => q.defer(null), /function/);
    assert.throws(() => q.defer(123), /function/);
    assert.throws(() => q.defer("notAFunction"), /function/);
  });

  it('calls error if one task errors and does not call twice', function(done) {
    let q = queue.queue();
    let errCount = 0;
    q.defer(makeTask(1));
    q.defer(makeTask(2, new Error('fail!')));
    q.defer(makeTask(3));
    q.awaitAll(function(err, results) {
      assert(err instanceof Error);
      assert.strictEqual(err.message, 'fail!');
      errCount++;
      setTimeout(() => {
        // The callback should _not_ be invoked again
        assert.strictEqual(errCount, 1);
        done();
      }, 5);
    });
  });

  it('throws if awaitAll is called twice', function() {
    const q = queue.queue();
    q.awaitAll(() => {});
    assert.throws(() => q.awaitAll(() => {}), /multiple await/);
  });

  it('does not invoke callback if no tasks', function(done) {
    let called = false;
    const q = queue.queue();
    q.awaitAll((err, results) => { called = true; assert.strictEqual(err, null); assert.deepStrictEqual(results, []); });
    setTimeout(() => {
      assert(called, 'should callback immediately with empty result');
      done();
    }, 5);
  });

  it('supports concurrency>1', function(done) {
    let finished = 0, results = [];
    const q = queue.queue(3);
    for (let i=0; i<3; ++i) {
      q.defer(cb => setTimeout(() => { results[i]=i*i; cb(null, i*i); }, 2*(i+1)));
    }
    q.awaitAll(function(err, r) {
      assert.strictEqual(err, null);
      assert.deepStrictEqual(r, [0,1,4]);
      done();
    });
  });

  it('handles sync exception thrown by queued task', function(done) {
    let q = queue.queue();
    q.defer(cb => { throw new Error('sync fail'); });
    q.awaitAll(function(err, results) {
      assert(err instanceof Error);
      assert.strictEqual(err.message, 'sync fail');
      done();
    });
  });

});