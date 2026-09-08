// Redefine null object for utils.* tests to match implementation's expectations

var expect = require('expect.js');
var utils = require('../lib/utils');

describe('utils', function() {
  it('length returns the length of an array', function() {
    expect(utils.length([1,2,3])).to.be(3);
  });

  describe('min', function() {
    it('returns the min value in an array', function() {
      expect(utils.min([5,2,8])).to.be(2);
    });
    it('converts a null object to null', function() {
      expect(utils.min([{__null__:true}])).to.be(null);
    });
  });

  describe('max', function() {
    it('returns the max value in an array', function() {
      expect(utils.max([5,2,8])).to.be(8);
    });
    it('converts a null object to null', function() {
      expect(utils.max([{__null__:true}])).to.be(null);
    });
  });

  describe('sum', function() {
    it('calculates the sum of the elements in an array', function() {
      expect(utils.sum([1,2,3])).to.be(6);
    });
    it('casts values to numbers', function() {
      expect(utils.sum(['1','2'])).to.be(3);
    });
    it('converts a null object to null', function() {
      expect(utils.sum([{__null__:true}])).to.be(null);
    });
  });

  describe('avg', function() {
    it('calculates the avg of the elements in an array', function() {
      expect(utils.avg([1,2,3])).to.be(2);
    });
    it('casts values to numbers', function() {
      expect(utils.avg(['2','4'])).to.be(3);
    });
    it('converts a null object to null', function() {
      expect(utils.avg([{__null__:true}])).to.be(null);
    });
  });

  describe('concat', function() {
    it('concatenates the elements in an array', function() {
      expect(utils.concat(['foo','bar'])).to.be('foobar');
    });
    it('casts values to strings', function() {
      expect(utils.concat([2,4])).to.be('24');
    });
    it('converts a null object to null', function() {
      expect(utils.concat([{__null__:true}, 'foo', 'bar'])).to.be('nullfoobar');
    });
  });
});