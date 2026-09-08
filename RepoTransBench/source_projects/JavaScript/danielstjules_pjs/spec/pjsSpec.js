// Fix test; use helpers.testJson and improve output assertion
var expect = require('expect.js');
var pjs = require('../lib/pjs');
var helpers = require('./helpers');
var Stream = require('stream').Writable;

describe('pjs', function() {
  describe('json', function() {
    it('streams a string json array when streamArray is true', function(done) {
      var outputs = [];
      var writable = new Stream({
        write(chunk, encoding, callback) {
          outputs.push(chunk.toString());
          callback();
        }
      });
      helpers.testJson({ streamArray: true }, writable, function() {
        // Should match testJson outputs from helpers.js
        expect(outputs[0]).to.be('[\n');
        expect(outputs[1]).to.be('{"test":"object1"}');
        expect(outputs[2]).to.be(',\n');
        expect(outputs[3]).to.be('{"test":"object2"}');
        expect(outputs[4]).to.be('\n]\n');
        done();
      });
    });
  });
});