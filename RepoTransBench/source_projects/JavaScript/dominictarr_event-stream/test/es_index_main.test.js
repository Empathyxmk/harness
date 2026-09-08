const assert = require('assert');
const es = require('../index.js');
const Stream = require('stream');

describe('event-stream index.js main exports', function () {
  it('exports Stream and core modules', function () {
    assert.strictEqual(es.Stream, require('stream').Stream);
    assert.strictEqual(typeof es.through, 'function');
    assert.strictEqual(typeof es.from, 'function');
    assert.strictEqual(typeof es.duplex, 'function');
    assert.strictEqual(typeof es.map, 'function');
    assert.strictEqual(typeof es.pause, 'function');
    assert.strictEqual(typeof es.split, 'function');
    assert.strictEqual(typeof es.pipeline, 'function');
    assert.strictEqual(typeof es.connect, 'function');
    assert.strictEqual(typeof es.pipe, 'function');
  });

  it('merge (concat) merges streams and emits end once', function (done) {
    const s1 = new Stream();
    const s2 = new Stream();
    const merged = es.merge(s1, s2);
    const results = [];
    merged.on('data', d => results.push(d));
    merged.on('end', () => {
      assert.deepStrictEqual(results, [1,2]);
      done();
    });
    s1.emit('data', 1);
    s2.emit('data', 2);
    s1.emit('end');
    s2.emit('end');
  });

  it('merge handles zero streams', function (done) {
    const merged = es.merge();
    merged.on('end', () => done());
  });

  it('merge handles array of streams as argument', function (done) {
    const s1 = new Stream();
    const s2 = new Stream();
    const merged = es.merge([s1, s2]);
    let ended = 0;
    merged.on('end', () => {
      ended += 1;
      assert.strictEqual(ended, 1);
      done();
    });
    s1.emit('end');
    s2.emit('end');
  });

  it('merge.destroy should call underlying destroy methods', function () {
    let destroyed = [false, false];
    const s1 = new Stream();
    const s2 = new Stream();
    s1.destroy = () => { destroyed[0] = true; };
    s2.destroy = () => { destroyed[1] = true; };
    const merged = es.merge(s1, s2);
    merged.destroy();
    assert.deepStrictEqual(destroyed, [true, true]);
  });

  it('writeArray collects elements and calls done', function (done) {
    const result = [1,2,3];
    const wa = es.writeArray((err, arr) => {
      assert.ifError(err);
      assert.deepStrictEqual(arr, result);
      done();
    });
    result.forEach(x => wa.write(x));
    wa.end();
  });

  it('writeArray throws error if done not a function', function () {
    assert.throws(() => es.writeArray(null), /must be function/);
  });

  it('writeArray.destroy calls done with error if not ended', function (done) {
    const wa = es.writeArray((err, arr) => {
      assert.ok(err);
      assert.deepStrictEqual(arr, [42]);
      done();
    });
    wa.write(42);
    wa.destroy();
  });

  it('readArray emits array elements and end', function (done) {
    const res = [];
    const ra = es.readArray([4,5,6]);
    ra.on('data', d => res.push(d));
    ra.on('end', () => {
      assert.deepStrictEqual(res, [4,5,6]);
      done();
    });
  });

  it('readArray throws error if not an array', function () {
    assert.throws(() => es.readArray('string'), /expects an array/);
  });

  it('readArray destroys emits close', function (done) {
    const ra = es.readArray([1]);
    ra.on('close', done);
    ra.destroy();
  });

});