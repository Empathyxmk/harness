const assert = require('chai').assert;
const uuid = require('uuid');
const nJwt = require('../');
const fs = require('fs');
const path = require('path');

function itShouldBeAValidJwt(jwt){
  assert(nJwt.create({}, uuid.v4()) instanceof nJwt.Jwt);
  let nowUnix = Math.floor(Date.now() / 1000);
  assert.equal(nJwt.create({}, uuid.v4()).body.iat , nowUnix);
  assert(jwt.body.jti.match(/[a-zA-Z0-9]+[-]/));
}

function testHmacAlg(alg, done){
  let key = uuid.v4().replace(/-/g,'XX');
  let claims = { goodbye: uuid.v4(), info: false };
  let jwt = nJwt.create(claims, key, alg);
  let token = jwt.compact();

  itShouldBeAValidJwt(jwt);

  nJwt.verify(token, key, alg, function(err, jwt){
    assert.isNull(err, 'Unexpected error returned');
    itShouldBeAValidJwt(jwt);
    done();
  });
}

// Only a sample HMAC, this can be extended with more algorithms if needed
describe("HMAC Algorithm Public Test", function(){
  it("should create and verify JWT with HS256 and different test data", function(done){
    testHmacAlg("HS256", done);
  });
});