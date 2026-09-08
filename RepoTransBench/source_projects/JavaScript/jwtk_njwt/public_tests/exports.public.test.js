const assert = require('chai').assert;
const nJwt = require('..');

describe('njwt module exports public', function () {
  it('should export classes with frozen prototypes (public)', function() {
    assert.isTrue(Object.isFrozen(nJwt.Jwt));
    assert.isTrue(Object.isFrozen(nJwt.Jwt.prototype));
    assert.isTrue(Object.isFrozen(nJwt.JwtBody));
    assert.isTrue(Object.isFrozen(nJwt.JwtBody.prototype));
    assert.isTrue(Object.isFrozen(nJwt.JwtHeader));
    assert.isTrue(Object.isFrozen(nJwt.JwtHeader.prototype));
    assert.isTrue(Object.isFrozen(nJwt.Verifier));
    assert.isTrue(Object.isFrozen(nJwt.Verifier.prototype));
  });

  it('should not allow prototype pollution (public)', function () {
    let token = `ewogICJ0eXAiOiAiUHVibGljSldUIiwKICAiYWxnIjogIk5vbmUiLAogICJfX3Byb3RvX18iOiB7CiAgICAidHlwIjogIkpXVCIsCiAgICAiYWxnIjogIkhTMzg0IiwKICAgICJfX3Byb3RvX18iOiB7ImNvbXBhY3QiOm51bGwsInJlc2VydmVkS2V5cyI6WyJpbmZvIl0KfQogIH0KfQ.ewogICJwdWIiOiAyLAogICJzY29wZSI6ICJ0ZXN0IiwKICAianRpIjogImE1MmNkY2Y2LTExZTktNDg1Zi05MDEwLWZlODc5MTkzMDQwNCIsCiAgImlhdCI6IDI1ODc0Nzg1MDYsCiAgImV4cCI6IDI1ODc0Nzg1MDYsCiAgIl9fcHJvdG9fXyI6IHsiY29tcGFjdCI6bnVsbCwidG9KU09OIjpudWxsLCJwb2xsdXRlZCI6dHJ1ZX19`.replace(/\s/g, '');
    assert.isOk(nJwt.JwtBody.prototype.hasOwnProperty('toJSON'));
    assert.isOk(nJwt.JwtBody.prototype.hasOwnProperty('compact'));
    assert.isOk(nJwt.JwtHeader.prototype.hasOwnProperty('compact'));

    nJwt.verify(token);

    assert.isOk(nJwt.JwtBody.prototype.hasOwnProperty('toJSON'));
    assert.isOk(nJwt.JwtBody.prototype.hasOwnProperty('compact'));
    assert.isOk(nJwt.JwtHeader.prototype.hasOwnProperty('compact'));
  });
});