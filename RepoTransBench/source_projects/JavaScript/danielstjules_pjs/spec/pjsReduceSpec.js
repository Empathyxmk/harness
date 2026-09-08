// Tests for reduce-related utils. Adjusted for min, max, avg, sum, concat edge cases.

var expect = require('expect.js');
var utils = require('../lib/utils');

describe('utils.min edge cases', function() {
  it('returns undefined for empty array', function() {
    expect(utils.min([])).to.be(undefined);
  });

  it('returns null for [null]', function() {
    expect(utils.min([null])).to.be(null);
  });
});

describe('utils.max edge cases', function() {
  it('returns undefined for empty array', function() {
    expect(utils.max([])).to.be(undefined);
  });

  it('returns null for [null]', function() {
    expect(utils.max([null])).to.be(null);
  });
});

describe('utils.avg edge cases', function() {
  it('returns undefined for empty array', function() {
    expect(utils.avg([])).to.be(undefined);
  });

  it('returns null for [null]', function() {
    expect(utils.avg([null])).to.be(null);
  });
});

describe('utils.concat edge cases', function() {
  it('returns null for [null]', function() {
    expect(utils.concat([null])).to.be(null);
  });
});