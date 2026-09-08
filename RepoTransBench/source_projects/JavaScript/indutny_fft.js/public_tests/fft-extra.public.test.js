'use strict';

const assert = require('assert');
const FFT = require('../lib/fft');

describe('FFT edge and error cases (public)', () => {
  it('should throw if transform output and input are the same (realTransform, diff size)', () => {
    const fft = new FFT(8);
    const arr = fft.createComplexArray();
    assert.throws(() => fft.realTransform(arr, arr), /must be different/);
  });

  it('should throw if inverseTransform output and input are the same (diff size)', () => {
    const fft = new FFT(16);
    const arr = fft.createComplexArray();
    assert.throws(() => fft.inverseTransform(arr, arr), /must be different/);
  });

  it('should throw if realTransform called with wrong length', () => {
    const fft = new FFT(8);
    const output = fft.createComplexArray();
    assert.throws(() => fft.realTransform(output, [1, 2, 3]), /length/);
  });

  it('should throw if completeSpectrum called with odd length', () => {
    const fft = new FFT(2);
    const arr = [1, 2, 3];
    assert.throws(() => fft.completeSpectrum(arr), /must be a complex array/);
  });

  it('should allow repeated use with different data', () => {
    const fft = new FFT(4);
    const a = fft.createComplexArray();
    const b = fft.toComplexArray([2, 4, 6, 8]);
    fft.transform(a, b);

    // Run again with different data
    const c = fft.createComplexArray();
    const d = fft.toComplexArray([8, 6, 4, 2]);
    fft.transform(c, d);

    assert.strictEqual(a.length, 8);
    assert.strictEqual(c.length, 8);
  });

  it('should return zeros for transform of all zeros (public)', () => {
    const fft = new FFT(4);
    const output = fft.createComplexArray();
    const input = fft.toComplexArray([0, 0, 0, 0]);
    fft.transform(output, input);

    for (let i = 0; i < output.length; i++) {
      assert.strictEqual(output[i], 0);
    }
  });

  it('should handle large size transform and inverse-transform with constant input (public)', () => {
    const n = 32;
    const fft = new FFT(n);
    const input = new Array(n);
    for (let i = 0; i < n; i++) input[i] = 7;
    const out = fft.createComplexArray();
    const data = fft.toComplexArray(input);
    fft.transform(out, data);
    fft.inverseTransform(data, out);

    // Should match original input
    for (let i = 0; i < n; i++) {
      assert(Math.abs(fft.fromComplexArray(data)[i] - 7) < 1e-10);
    }
  });
});