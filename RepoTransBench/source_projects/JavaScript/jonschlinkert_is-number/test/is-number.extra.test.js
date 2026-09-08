'use strict';

const assert = require('assert');
const isNumber = require('../index');

describe('additional is-number coverage', function() {
  it('should return false for non-string, non-number argument (object)', function() {
    assert.strictEqual(isNumber({ a: 1 }), false);
  });

  it('should return false for undefined', function() {
    assert.strictEqual(isNumber(undefined), false);
  });

  it('should return false for null', function() {
    assert.strictEqual(isNumber(null), false);
  });

  it('should return false for an array', function() {
    assert.strictEqual(isNumber([1,2]), false);
  });

  it('should return false for empty string', function() {
    assert.strictEqual(isNumber(''), false);
  });

  it('should return false for whitespace string', function() {
    assert.strictEqual(isNumber('   '), false);
  });

  it('should return false for string with non-numeric value', function() {
    assert.strictEqual(isNumber('foo'), false);
  });

  it('should return false for NaN', function() {
    assert.strictEqual(isNumber(NaN), false);
  });

  it('should handle Number.isFinite polyfill', function() {
    const original = Number.isFinite;
    Number.isFinite = undefined;
    assert.strictEqual(isNumber('123'), true);
    Number.isFinite = original;
  });

  it('should return true for numbers with leading/trailing whitespace', function() {
    assert.strictEqual(isNumber(' 42 '), true);
  });
});