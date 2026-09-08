const assert = require('assert');
const queue = require('../src/queue.cjs');

function makeTask(value, error) {
  return function(cb) {
    setTimeout(() => {
      if (error) cb(error);
      else cb(null, value);
    }, 2); // different delay than original for data difference
  };
}

describe('Queue CJS Extra - public', function() {

  it('throws if defer argument is not a function - different types', function() {
    const q = queue.queue();
    assert.throws(() => q.defer(undefined), /function/);
    assert.throws(() => q.defer({}), /function/);
    assert.throws(() => q.defer([]), /function/);
  });

  it('calls error if one task errors and does not call twice (different error)', function(done) {
    let q = queue.queue();
    let errCount = 0;
    q.defer(makeTask('a'));
    q.defer(makeTask('b', new Error('boom!')));
    q.defer(makeTask('c'));
    q.awaitAll(function(err, results) {
      assert(err instanceof Error);
      assert.strictEqual(err.message, 'boom!');
      errCount++;
      setTimeout(() => {
        assert.strictEqual(errCount, 1);
        done();
      }, 5);
    });
  });

  it('throws if awaitAll is called twice (public ver)', function() {
    const q = queue.queue();
    q.awaitAll(() => {});
    assert.throws(() => q.awaitAll(() => {}), /multiple await/);
  });

  it('does not invoke callback if zero tasks (public)', function(done) {
    let called = false;
    const q = queue.queue();
    q.awaitAll((err, results) => { called = true; assert.strictEqual(err, null); assert.deepStrictEqual(results, []); });
    setTimeout(() => {
      assert(called, 'should callback immediately with empty result');
      done();
    }, 3);
  });

  it('supports concurrency>1 (different data)', function(done) {
    let finished = 0, results = [];
    const q = queue.queue(2);
    for (let i=0; i<2; ++i) {
      q.defer(cb => setTimeout(() => { results[i]=i+10; cb(null, i+10); }, 3*(i+1)));
    }
    q.awaitAll(function(err, r) {
      assert.strictEqual(err, null);
      assert.deepStrictEqual(r, [10,11]);
      done();
    });
  });

  it('handles sync exception thrown by queued task (different error)', function(done) {
    let q = queue.queue();
    q.defer(cb => { throw new Error('public sync fail'); });
    q.awaitAll(function(err, results) {
      assert(err instanceof Error);
      assert.strictEqual(err.message, 'public sync fail');
      done();
    });
  });

});