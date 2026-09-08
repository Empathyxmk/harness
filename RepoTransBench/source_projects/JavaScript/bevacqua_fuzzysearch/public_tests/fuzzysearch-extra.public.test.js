'use strict';

const fuzzysearch = require('..');
const assert = require('assert');

describe('fuzzysearch edge cases and branches (public tests)', () => {
  it('should return false when needle is longer than haystack', () => {
    assert.strictEqual(fuzzysearch('helloworld', 'hello'), false);
    assert.strictEqual(fuzzysearch('abcdefg', 'abcd'), false);
    assert.strictEqual(fuzzysearch('🍔🍟🍕', '🍟🍕'), false);
  });

  it('should return true when needle equals haystack', () => {
    assert.strictEqual(fuzzysearch('bar', 'bar'), true);
    assert.strictEqual(fuzzysearch(' ', ' '), true);
    assert.strictEqual(fuzzysearch('🍟', '🍟'), true);
  });

  it('should return true for empty needle', () => {
    assert.strictEqual(fuzzysearch('', 'public'), true);
    assert.strictEqual(fuzzysearch('', 'a'), true);
  });

  it('should match consecutive characters (successful path)', () => {
    assert.strictEqual(fuzzysearch('xyz', 'xxxyyyzzzxyzxyz'), true);
  });

  it('should handle mismatches properly', () => {
    assert.strictEqual(fuzzysearch('bzz', 'baz'), false);
    assert.strictEqual(fuzzysearch('p', 'o'), false);
    assert.strictEqual(fuzzysearch('x', ''), false);
  });

  it('should be case sensitive', () => {
    assert.strictEqual(fuzzysearch('Bar', 'bar'), false);
    assert.strictEqual(fuzzysearch('bar', 'Bar'), false);
    assert.strictEqual(fuzzysearch('BAR', 'bar'), false);
  });

  it('should handle haystack with special or unicode chars', () => {
    assert.strictEqual(fuzzysearch('好', '你好吗'), true);
    assert.strictEqual(fuzzysearch('吗', '你好'), false);
    assert.strictEqual(fuzzysearch('ñ', 'ñ'), false); // different unicode composed/decomposed
  });

  it('should return false if needle has char not in haystack (full scan)', () => {
    assert.strictEqual(fuzzysearch('q', 'uvw'), false);
    assert.strictEqual(fuzzysearch('🚀', '🌟🚀'), true);
    assert.strictEqual(fuzzysearch('🚀🌟', '🌟🚀'), false);
  });
});