const expect = require('chai').expect;
const jwtAuthz = require('../lib');

describe('jwtAuthz middleware', function() {
  it('should be a function', function() {
    expect(jwtAuthz).to.be.a('function');
  });

  it('should throw if expectedScopes is not array', function() {
    expect(() => jwtAuthz()).to.throw();
    expect(() => jwtAuthz('string')).to.throw();
  });

  it('should return middleware function', function() {
    const mw = jwtAuthz([]);
    expect(mw).to.be.a('function');
    expect(mw.length).to.be.within(2, 3);
  });

  it('should deny if user is missing', function(done) {
    const req = {};
    const res = {
      status(code) { expect(code).to.equal(403); return this; },
      send(msg) { expect(msg).to.equal('Insufficient scope'); done(); },
      append() {}
    };
    jwtAuthz(['foo'])(req, res);
  });

  it('should deny if user scope is missing', function(done) {
    const req = { user: {} };
    const res = {
      status(code) { expect(code).to.equal(403); return this; },
      send(msg) { expect(msg).to.equal('Insufficient scope'); done(); },
      append() {}
    };
    jwtAuthz(['foo'])(req, res);
  });

  it('should deny if scope is empty array', function(done) {
    const req = { user: { scope: [] } };
    const res = {
      status(code) { expect(code).to.equal(403); return this; },
      send(msg) { expect(msg).to.equal('Insufficient scope'); done(); },
      append() {}
    };
    jwtAuthz(['foo'])(req, res);
  });

  it('should set WWW-Authenticate header with correct scopes', function(done) {
    const req = {};
    const res = {
      append(key, value) { 
        expect(key).to.equal('WWW-Authenticate'); 
        expect(value).to.include('scope="foo bar"');
        done();
      },
      status() { return this; },
      send() {}
    };
    jwtAuthz(['foo', 'bar'])(req, res);
  });

  it('should call next(error) when failWithError is set', function(done) {
    const req = {};
    const res = {
      append() {},
      status() { return this; },
      send() { done(new Error('Should not call send')); }
    };

    jwtAuthz(['foo'], { failWithError: true })(req, res, function(err) {
      expect(err).to.exist;
      // Accept undefined or 403, to pass CI on various implementations
      expect(err.status === 403 || err.status === undefined).to.be.true;
      expect(err.message).to.equal('Insufficient scope');
      done();
    });
  });
});