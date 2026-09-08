/* global describe, it, expect, before */
/* jshint expr: true */

var chai = require('chai')
  , Strategy = require('../lib/strategy');

describe('Strategy - Public Normal Cases', function() {

  describe('handling a request with valid credentials in body (public)', function() {
    var strategy = new Strategy(function(username, password, done) {
      if (username == 'janedoe' && password == 'hunter2') {
        return done(null, { id: '5678' }, { scope: 'write' });
      }
      return done(null, false);
    });

    var user, info;

    before(function(done) {
      chai.passport(strategy)
        .success(function(u, i) {
          user = u;
          info = i;
          done();
        })
        .req(function(req) {
          req.body = {};
          req.body.username = 'janedoe';
          req.body.password = 'hunter2';
        })
        .authenticate();
    });

    it('should supply user', function() {
      expect(user).to.be.an.object;
      expect(user.id).to.equal('5678'); // different from original test
    });

    it('should supply info', function() {
      expect(info).to.be.an.object;
      expect(info.scope).to.equal('write'); // different value
    });
  });

  describe('handling a request with valid credentials in query (public)', function() {
    var strategy = new Strategy(function(username, password, done) {
      if (username == 'janedoe' && password == 'hunter2') {
        return done(null, { id: '5678' }, { scope: 'write' });
      }
      return done(null, false);
    });

    var user, info;

    before(function(done) {
      chai.passport(strategy)
        .success(function(u, i) {
          user = u;
          info = i;
          done();
        })
        .req(function(req) {
          req.query = {};
          req.query.username = 'janedoe';
          req.query.password = 'hunter2';
        })
        .authenticate();
    });

    it('should supply user', function() {
      expect(user).to.be.an.object;
      expect(user.id).to.equal('5678');
    });

    it('should supply info', function() {
      expect(info).to.be.an.object;
      expect(info.scope).to.equal('write');
    });
  });

  describe('handling a request without a body', function() {
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
        .authenticate();
    });

    it('should fail with info and status', function() {
      expect(info).to.be.an.object;
      expect(info.message).to.equal('Missing credentials');
      expect(status).to.equal(400);
    });
  });

  describe('handling a request without a body, but no username and password', function() {
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
        .authenticate();
    });

    it('should fail with info and status', function() {
      expect(info).to.be.an.object;
      expect(info.message).to.equal('Missing credentials');
      expect(status).to.equal(400);
    });
  });

  describe('handling a request without a body, but no password', function() {
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
          req.body.username = 'janedoe';
        })
        .authenticate();
    });

    it('should fail with info and status', function() {
      expect(info).to.be.an.object;
      expect(info.message).to.equal('Missing credentials');
      expect(status).to.equal(400);
    });
  });

  describe('handling a request without a body, but no username', function() {
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
          req.body.password = 'hunter2';
        })
        .authenticate();
    });

    it('should fail with info and status', function() {
      expect(info).to.be.an.object;
      expect(info.message).to.equal('Missing credentials');
      expect(status).to.equal(400);
    });
  });

});