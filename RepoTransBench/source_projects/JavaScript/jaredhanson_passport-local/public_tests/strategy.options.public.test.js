/* global describe, it, expect, before */
/* jshint expr: true */

var chai = require('chai')
  , Strategy = require('../lib/strategy');


describe('Strategy - Public Option Cases', function() {

  describe('handling a request without a body, but no username and password, with message option to authenticate (public)', function() {
    var strategy = new Strategy(function(username, password, done) {
      throw new Error('should not be called - public');
    });

    var info, status;

    before(function(done) {
      chai.passport(strategy)
        .fail(function(i, s) {
          info = i;
          status = s;
          done();
        })
        .req(function(req) {
          req.body = {};
        })
        .authenticate({ badRequestMessage: 'Request is malformed (public)' });
    });

    it('should fail with info and status', function() {
      expect(info).to.be.an.object;
      expect(info.message).to.equal('Request is malformed (public)');
      expect(status).to.equal(400);
    });
  });

});