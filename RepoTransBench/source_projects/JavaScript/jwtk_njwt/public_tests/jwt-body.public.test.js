const assert = require('chai').assert;
const nJwt = require('../');
describe('JwtBody Public', function() {
  it('should construct JwtBody from call without new', function() {
    assert(nJwt.JwtBody() instanceof nJwt.JwtBody);
  });
});