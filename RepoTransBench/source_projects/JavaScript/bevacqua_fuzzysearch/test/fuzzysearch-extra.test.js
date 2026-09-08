'use strict';

const fuzzysearch = require('..');
const assert = require('assert');

describe('fuzzysearch edge cases and branches', () => {
  it('should return false when needle is longer than haystack', () => {
    assert.strictEqual(fuzzysearch('foobar', 'foo'), false);
    assert.strictEqual(fuzzysearch('abcde', 'abcd'), false);
    assert.strictEqual(fuzzysearch('🍕🍟', '🍕'), false);
  });

  it('should return true when needle equals haystack', () => {
    assert.strictEqual(fuzzysearch('foo', 'foo'), true);
    assert.strictEqual(fuzzysearch('', ''), true);
    assert.strictEqual(fuzzysearch('🍕', '🍕'), true);
  });

  it('should return true for empty needle', () => {
    assert.strictEqual(fuzzysearch('', 'something'), true);
    assert.strictEqual(fuzzysearch('', ''), true);
  });

  it('should match consecutive characters (successful path)', () => {
    assert.strictEqual(fuzzysearch('abc', 'aabbccabcabc'), true);
  });

  it('should handle mismatches properly', () => {
    assert.strictEqual(fuzzysearch('axx', 'abx'), false);
    assert.strictEqual(fuzzysearch('b', 'a'), false);
    assert.strictEqual(fuzzysearch('a', ''), false);
  });

  it('should be case sensitive', () => {
    assert.strictEqual(fuzzysearch('Foo', 'foo'), false);
    assert.strictEqual(fuzzysearch('foo', 'Foo'), false);
    assert.strictEqual(fuzzysearch('FOO', 'foo'), false);
  });

  it('should handle haystack with special or unicode chars', () => {
    assert.strictEqual(fuzzysearch('你', '你好'), true);
    assert.strictEqual(fuzzysearch('你', '再见'), false);
    assert.strictEqual(fuzzysearch('e\u0301', 'é'), false); // composed vs decomposed
  });

  it('should return false if needle has char not in haystack (full scan)', () => {
    assert.strictEqual(fuzzysearch('z', 'abc'), false);
    assert.strictEqual(fuzzysearch('🙂', '🙃🙂'), true);
    assert.strictEqual(fuzzysearch('🙂🙃', '🙃🙂'), false);
  });
});