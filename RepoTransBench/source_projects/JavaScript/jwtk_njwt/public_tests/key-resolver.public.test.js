const assert = require('chai').assert;
const uuid = require('uuid');
const nJwt = require('../');
const properties = require('../properties.json');

describe('Verifier Public', function() {
  it('should construct Verifier without new', function() {
    assert(nJwt.Verifier() instanceof nJwt.Verifier);
  });

  describe('.withKeyResolver()', function() {
    let resolver;
    before(function() {
      resolver = function() {};
    });

    it('should set keyResolver field', function() {
      let jwtVerifier = new nJwt.Verifier();
      jwtVerifier.withKeyResolver(resolver);
      assert.isDefined(jwtVerifier.keyResolver);
    });

    it('should return the Verifier object (public test)', function() {
      let jwtVerifier = new nJwt.Verifier();
      assert(jwtVerifier.withKeyResolver(function() {}) === jwtVerifier);
    });
  });
});