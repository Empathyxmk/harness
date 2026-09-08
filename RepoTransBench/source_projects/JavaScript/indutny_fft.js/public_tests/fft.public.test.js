'use strict';

const assert = require('assert');
const FFT = require('../lib/fft');

// Helper to fix rounding for approximate comparison
function fixRoundEqual(actual, expected) {
  function fixRound(r) {
    return Math.round(r * 10000) / 10000;
  }

  assert.strictEqual(actual.map(fixRound).join(':'), expected.map(fixRound).join(':'));
}

describe('FFT.js (public tests)', () => {
  it('should compute tables (different size)', () => {
    const f = new FFT(16);

    assert.strictEqual(f.table.length, 32);
  });

  it('should throw on another set of invalid table sizes', () => {
    assert.throws(() => {
      new FFT(5);
    }, /power of two/);

    assert.throws(() => {
      new FFT(-8);
    }, /power of two/);

    assert.throws(() => {
      new FFT(0);
    }, /power of two/);

    assert.throws(() => {
      new FFT(3);
    }, /power of two/);

    assert.throws(() => {
      new FFT(13);
    }, /power of two/);
  });

  it('should create complex array of different size', () => {
    const f = new FFT(2);

    assert.strictEqual(f.createComplexArray().length, 4);
    assert.strictEqual(f.createComplexArray()[2], 0);
  });

  it('should convert to complex array with different numeric data', () => {
    const f = new FFT(2);

    assert.deepEqual(f.toComplexArray([10, 20]), [10, 0, 20, 0]);
  });

  it('should convert from complex array (different data)', () => {
    const f = new FFT(2);

    assert.deepEqual(f.fromComplexArray(f.toComplexArray([6, 8])), [6, 8]);
  });

  it('should throw on invalid transform inputs, new case', () => {
    const f = new FFT(4);
    const output = f.createComplexArray();

    assert.throws(() => {
      f.transform(output, output);
    }, /must be different/);
  });

  it('should transform trivial radix-2 case with new inputs', () => {
    const f = new FFT(2);

    const out = f.createComplexArray();
    let data = f.toComplexArray([2, -2]);
    f.transform(out, data);
    assert.deepEqual(out, [0, 0, 4, 0]);

    data = f.toComplexArray([10, 10]);
    f.transform(out, data);
    assert.deepEqual(out, [20, 0, 0, 0]);

    // Linear combination (all negative)
    data = f.toComplexArray([-1, 0]);
    f.transform(out, data);
    assert.deepEqual(out, [-1, 0, -1, 0]);
  });

  it('should transform another trivial case', () => {
    const f = new FFT(4);

    const out = f.createComplexArray();
    let data = f.toComplexArray([3, 1, 0, -1]);
    f.transform(out, data);
    fixRoundEqual(out, [3, 0, 3, -2.8284, 3, 0, 3, 2.8284]);

    data = f.toComplexArray([2, 0, -2, 0]);
    f.transform(out, data);
    assert.deepEqual(out, [0, 0, 4, 0, 0, 0, 4, 0]);
  });

  it('should inverse-transform with alternate data', () => {
    const f = new FFT(4);

    const out = f.createComplexArray();
    const data = f.toComplexArray([4, 3, 2, 1]);
    f.transform(out, data);
    fixRoundEqual(out, [10, 0, 2, 2, -2, 0, 2, -2]);
    f.inverseTransform(data, out);
    assert.deepEqual(f.fromComplexArray(data), [4, 3, 2, 1]);
  });

  it('should transform bigger recursive case (different values)', () => {
    const input = [];
    for (let i = 0; i < 64; i++)
      input.push(i * 2);

    const f = new FFT(input.length);

    const out = f.createComplexArray();
    let data = f.toComplexArray(input);
    f.transform(out, data);
    f.inverseTransform(data, out);
    fixRoundEqual(f.fromComplexArray(data), input);
  });

  it('should transform big recursive radix-2 case (different values)', () => {
    const input = [];
    for (let i = 0; i < 32; i++)
      input.push(i * 3);

    const f = new FFT(input.length);

    const out = f.createComplexArray();
    let data = f.toComplexArray(input);
    f.transform(out, data);
    f.inverseTransform(data, out);
    fixRoundEqual(f.fromComplexArray(data), input);
  });
});