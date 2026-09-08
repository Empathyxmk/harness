// Comprehensive tests for is-number covering edge cases and core paths
'use strict';
const assert = require('assert');
const isNumber = require('../index');

describe('is-number (comprehensive)', function() {
  it('should return true for integer strings', function() {
    assert.strictEqual(isNumber('123'), true);
    assert.strictEqual(isNumber('-123'), true);
    assert.strictEqual(isNumber('+123'), true);
  });
  it('should return true for normal numbers', function() {
    assert.strictEqual(isNumber(123), true);
    assert.strictEqual(isNumber(-123), true);
    assert.strictEqual(isNumber(0), true);
  });
  it('should return false for numeric but not finite values', function() {
    assert.strictEqual(isNumber(Infinity), false);
    assert.strictEqual(isNumber(-Infinity), false);
    assert.strictEqual(isNumber(NaN), false);
    assert.strictEqual(isNumber('NaN'), false);
  });
  it('should return true for floats', function() {
    assert.strictEqual(isNumber(3.14), true);
    assert.strictEqual(isNumber('3.14'), true);
  });
  it('should return true for scientific notation', function() {
    assert.strictEqual(isNumber('1e3'), true);
    assert.strictEqual(isNumber('-1e-3'), true);
    assert.strictEqual(isNumber('0.1e+2'), true);
  });
  it('should return false for strings with spaces mid-value', function() {
    assert.strictEqual(isNumber('1 2 3'), false);
    assert.strictEqual(isNumber('1 2'), false);
    assert.strictEqual(isNumber('1. 0'), false);
  });
  it('should return false for non-numeric strings', function() {
    assert.strictEqual(isNumber('abc'), false);
    assert.strictEqual(isNumber('123abc'), false);
    assert.strictEqual(isNumber('abc123'), false);
    assert.strictEqual(isNumber('++123'), false);
    assert.strictEqual(isNumber('--123'), false);
    assert.strictEqual(isNumber(' 123abc'), false);
    assert.strictEqual(isNumber('abc123 '), false);
    // Remove hex/bin/octal strings from here (see below)
  });
  it('should return false for objects, arrays, null, undefined', function() {
    assert.strictEqual(isNumber([]), false);
    assert.strictEqual(isNumber({}), false);
    assert.strictEqual(isNumber(undefined), false);
    assert.strictEqual(isNumber(null), false);
    assert.strictEqual(isNumber(new Date()), false);
  });
  it('should return false for boolean values', function() {
    assert.strictEqual(isNumber(true), false);
    assert.strictEqual(isNumber(false), false);
  });
  it('should return false for empty and whitespace-only strings', function() {
    assert.strictEqual(isNumber(''), false);
    assert.strictEqual(isNumber('   '), false);
    assert.strictEqual(isNumber('\n\t'), false);
  });
  it('should return false for number objects containing a number', function() {
    // In this lib, isNumber(Object(1)) is false, see README
    assert.strictEqual(isNumber(Object(1)), false);
    assert.strictEqual(isNumber(Object(3.14)), false);
    // And still false for non-number objects
    assert.strictEqual(isNumber(Object('1')), false);
  });
  it('should return false for functions', function() {
    assert.strictEqual(isNumber(function(){}), false);
    assert.strictEqual(isNumber(() => 1), false);
  });
  it('should return true for hexadecimal, binary, octal numeric strings if Number() is finite', function() {
    // According to this lib, hex is number if Number("0xff") is finite (returns 255)
    assert.strictEqual(isNumber('0x11'), true);
    assert.strictEqual(isNumber('0b11'), true);
    assert.strictEqual(isNumber('0o11'), true);
    assert.strictEqual(isNumber('0xGHI'), false);
  });
  it('should handle Number.isFinite polyfills/overrides gracefully', function() {
    const orig = Number.isFinite;
    delete Number.isFinite;
    assert.strictEqual(isNumber(45), true);
    Number.isFinite = orig;
  });
});