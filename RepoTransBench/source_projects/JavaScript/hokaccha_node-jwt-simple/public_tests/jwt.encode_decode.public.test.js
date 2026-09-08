const expect = require('expect.js');
const jwt = require('../lib/jwt');
const fs = require('fs');
const path = require('path');

describe('jwt encode/decode (public)', function () {
  it('should encode and decode with HS384', function () {
    const secret = 'public secret';
    const payload = { baz: 'qux', iat: Math.floor(Date.now() / 1000) + 10 };
    const token = jwt.encode(payload, secret, 'HS384');
    const decoded = jwt.decode(token, secret, false, 'HS384');
    expect(decoded.baz).to.equal('qux');
  });

  it('should throw with wrong secret for HS384', function () {
    const secret = 'another secret';
    const payload = { abc: 'xyz', iat: Math.floor(Date.now() / 1000) + 20 };
    const token = jwt.encode(payload, secret, 'HS384');
    expect(function () {
      jwt.decode(token, 'not the secret', false, 'HS384');
    }).to.throwError();
  });

  it('should encode and decode with default algorithm and new payload', function () {
    const secret = 'extra secret';
    const payload = { hi: 'public' };
    const token = jwt.encode(payload, secret);
    const decoded = jwt.decode(token, secret);
    expect(decoded.hi).to.equal('public');
  });

  it('should support different additional header fields', function () {
    const secret = 'another secret';
    const payload = { publicProperty: 79 };
    const header = { kid: 'pubkey-1', test: 'ok' };
    const token = jwt.encode(payload, secret, 'HS384', { header: header });
    const decoded = jwt.decode(token, secret, false, 'HS384');
    const tokenParts = token.split('.');
    const decodedHeader = JSON.parse(Buffer.from(tokenParts[0], 'base64').toString());
    expect(decodedHeader.kid).to.equal('pubkey-1');
    expect(decodedHeader.test).to.equal('ok');
    expect(decoded.publicProperty).to.equal(79);
  });

  it('should decode with "no verify" flag on HS512', function () {
    const secret = 'novverify';
    const payload = { hello: 'decode-any', iat: Math.floor(Date.now() / 1000) + 100 };
    const token = jwt.encode(payload, secret, 'HS512');
    const decoded = jwt.decode(token, secret, true);
    expect(decoded.hello).to.equal('decode-any');
  });

  it('should throw on bad token format with 1 dot only', function () {
    expect(function () {
      jwt.decode('onepart.only', 'pub');
    }).to.throwError();
  });

  it('should throw if algorithm "skip" is not supported', function () {
    const secret = 'failsecret';
    const payload = { test: 'fail' };
    expect(function () {
      jwt.encode(payload, secret, 'SKIPME');
    }).to.throwError();
  });

  it('should throw if decoding unsupported algorithm "LOL"', function () {
    const secret = 'failsecret2';
    const payload = { test: 'failagain' };
    const header = { alg: 'LOL', typ: 'JWT' };
    const segments = [
      Buffer.from(JSON.stringify(header)).toString('base64').replace(/=/g,""),
      Buffer.from(JSON.stringify(payload)).toString('base64').replace(/=/g,""),
      "somesig"
    ];
    const token = segments.join(".");
    expect(() => jwt.decode(token, secret)).to.throwError();
  });

  it('should throw if verifying RS512 with no key', function () {
    // Just as before, encode with RS512, decode with empty key
    const payload = { what: 'ever' };
    const privKey = fs.readFileSync(path.join(__dirname, '..', 'test', 'test.pem'));
    const token = jwt.encode(payload, privKey, 'RS512');
    expect(function () {
      jwt.decode(token, '', false, 'RS512');
    }).to.throwError();
  });

  it('should encode and decode with RS512', function () {
    const privateKey = fs.readFileSync(path.join(__dirname, '..', 'test', 'test.pem'));
    const publicKey = fs.readFileSync(path.join(__dirname, '..', 'test', 'test.crt'));
    const payload = { foo: 'barbaz', n: 1234 };
    const token = jwt.encode(payload, privateKey, 'RS512');
    const decoded = jwt.decode(token, publicKey, false, 'RS512');
    expect(decoded.foo).to.equal('barbaz');
    expect(decoded.n).to.equal(1234);
  });

  it('should throw for another malformed base64/JSON', function () {
    // Same logic, but different structure/keys
    const token =
      Buffer.from('{"alg":"HS512"}').toString('base64') +
      '.' +
      Buffer.from('{badstuff!}').toString('base64') +
      '.' +
      'pubsig';
    expect(function () {
      jwt.decode(token, 'secrethere', true);
    }).to.throwError();
  });

  it('should accept empty array payload', function () {
    const secret = 'arraypass';
    const payload = [];
    const token = jwt.encode(payload, secret);
    const decoded = jwt.decode(token, secret);
    expect(decoded).to.eql([]);
  });
});