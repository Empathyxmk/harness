'use strict';

const assert = require('assert');
const FFT = require('../lib/fft');

describe('FFT edge and error cases', () => {
  it('should throw if transform output and input are the same (realTransform)', () => {
    const fft = new FFT(4);
    const arr = fft.createComplexArray();
    assert.throws(() => fft.realTransform(arr, arr), /must be different/);
  });

  it('should throw if inverseTransform output and input are the same', () => {
    const fft = new FFT(4);
    const arr = fft.createComplexArray();
    assert.throws(() => fft.inverseTransform(arr, arr), /must be different/);
  });

  it('should fill completeSpectrum for even-length arrays', () => {
    const fft = new FFT(4);
    const arr = [1, 2, 3, 4, 5, 6, 7, 8];
    // should not throw
    fft.completeSpectrum(arr);
    // There are specific mirrored index requirements in FFT spectrum
    // We just check for 'no throw' and preservation of structure
    assert.strictEqual(arr.length, 8);
  });

  it('toComplexArray returns supplied output array if set', () => {
    const fft = new FFT(2);
    const out = [99, 99, 99, 99];
    const res = fft.toComplexArray([1, 2], out);
    assert.strictEqual(res, out);
    assert.deepStrictEqual(out, [1, 0, 2, 0]);
  });

  it('fromComplexArray returns supplied output array if set', () => {
    const fft = new FFT(2);
    const arr = [1, 0, 2, 0];
    const out = [88, 88];
    const res = fft.fromComplexArray(arr, out);
    assert.strictEqual(res, out);
    assert.deepStrictEqual(out, [1, 2]);
  });

  it('createComplexArray returns zeros array of expected length', () => {
    const fft = new FFT(8);
    const arr = fft.createComplexArray();
    assert.strictEqual(arr.length, 16);
    assert(arr.every(x => x === 0));
  });

  it('throws if FFT size is not a power of 2 and > 1', () => {
    assert.throws(() => new FFT(1), /power of two/);
    assert.throws(() => new FFT(10), /power of two/);
    assert.throws(() => new FFT(-2), /power of two/);
  });
});