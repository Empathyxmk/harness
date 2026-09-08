const assert = require('chai').assert;
const nJwt = require('../');
const uuid = require('uuid');
const properties = require('../properties.json');

describe('Jwt Public', function() {
  it('should construct itself if called as function', function() {
    assert(nJwt.Jwt() instanceof nJwt.Jwt);
  });

  describe('.setClaim() public', function() {
    it('should set a different claim value', function() {
      let claimValue = uuid.v4().replace(/-/g, "#");
      assert.equal(nJwt.Jwt().setClaim('publicClaim', claimValue).body.publicClaim, claimValue);
    });
  });

  describe('.setHeader()', function() {
    it('should set another header param', function() {
      let kid = uuid.v4().substring(0, 8);
      assert.equal(nJwt.Jwt().setHeader('publicKid', kid).header.publicKid, kid);
    });
  });

  describe('.setSubject()', function() {
    it('should set the sub claim with a new value', function() {
      let sub = "user-" + uuid.v1();
      assert.equal(nJwt.Jwt().setSubject(sub).body.sub, sub);
    });
  });

  describe('.setIssuer()', function() {
    it('should set the iss claim with a different value', function() {
      let iss = "issuer-public-" + uuid.v1();
      assert.equal(nJwt.Jwt().setIssuer(iss).body.iss, iss);
    });
  });

  describe('.setExpiration()', function() {
    it('should accept a valid Date and set exp', function() {
      let d = new Date(Date.now() + 99999);
      assert.equal(nJwt.Jwt().setExpiration(d).body.exp, Math.floor(d.getTime() / 1000));
    });
  });
});