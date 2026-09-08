const assert = require('chai').assert;
const nJwt = require('../');
const uuid = require('uuid');
const properties = require('../properties.json');

describe('Jwt() Public', function() {
  describe('signWith()', function() {
    describe('if called with an invalid algorithm', function() {
      it('should throw for non-existent alg', function() {
        assert.throws(function() {
          new nJwt.Jwt().setSigningAlgorithm('invalid-alg');
        }, properties.errors.UNSUPPORTED_SIGNING_ALG);
      });
    });
  });
});

describe('create() Public', function() {
  it('should throw SIGNING_KEY_REQUIRED if called without any args', function() {
    assert.throws(function() {
      nJwt.create();
    }, properties.errors.SIGNING_KEY_REQUIRED);
  });

  it('should create a default token if the secret is a random string', function() {
    assert(nJwt.create(uuid.v4().replace(/[0-9]/g, 'z')) instanceof nJwt.Jwt);
  });

  it('should throw if defaults used and secret key not provided', function() {
    assert.throws(function() {
      nJwt.create({active: true});
    }, properties.errors.SIGNING_KEY_REQUIRED);
  });

  it('should not throw when no options, empty object omitted, but secret provided', function() {
    assert.doesNotThrow(function() {
      nJwt.create('mySecretPublicTest');
    });
  });
});