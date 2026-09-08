'use strict';

const assert = require('assert');
const isNumber = require('../index');

describe('additional is-number public coverage', function() {
  it('should return false for non-string, non-number argument (symbol)', function() {
    assert.strictEqual(isNumber(Symbol('a')), false);
  });

  it('should return false for a function', function() {
    assert.strictEqual(isNumber(function() {}), false);
  });

  it('should return false for boolean true', function() {
    assert.strictEqual(isNumber(true), false);
  });

  it('should return false for an array with three elements', function() {
    assert.strictEqual(isNumber([7, 8, 9]), false);
  });

  it('should return false for a string with only tabs', function() {
    assert.strictEqual(isNumber('\t\t\t'), false);
  });

  it('should return false for string with newline and spaces', function() {
    assert.strictEqual(isNumber('\n   '), false);
  });

  it('should return false for string with alphanumeric value', function() {
    assert.strictEqual(isNumber('123abc'), false);
  });

  it('should return false for negative NaN', function() {
    assert.strictEqual(isNumber(-NaN), false);
  });

  it('should handle Number.isFinite polyfill for negative numbers', function() {
    const original = Number.isFinite;
    Number.isFinite = undefined;
    assert.strictEqual(isNumber('-321'), true);
    Number.isFinite = original;
  });

  it('should return true for numbers inside string with newline', function() {
    assert.strictEqual(isNumber('\n58\n'), true);
  });
});