const jwt = require('../index');
const fs = require('fs');
const path = require('path');

describe('sign.js and verify.js additional coverage', () => {
  const secret = 'shhhhh';

  it('signs and verifies a token using HS256', done => {
    const payload = { foo: 'bar' };
    jwt.sign(payload, secret, { algorithm: 'HS256' }, (err, token) => {
      expect(err).toBeNull();
      expect(typeof token).toBe('string');
      jwt.verify(token, secret, { algorithms: ['HS256'] }, (err, decoded) => {
        expect(err).toBeNull();
        expect(decoded.foo).toBe('bar');
        done();
      });
    });
  });

  it('throws if options contains unknown key', () => {
    expect(() => {
      jwt.sign({foo:'bar'}, secret, {unknownOption: true});
    }).toThrow(/is not allowed in "options"/);
  });

  it('throws if payload is not object', () => {
    expect(() => {
      jwt.sign(null, secret, {});
    }).toThrow();
    expect(() => {
      jwt.sign('stringpayload', secret, {});
    }).not.toThrow();
  });

  it('throws if options property is wrong type', () => {
    expect(() => {
      jwt.sign({foo:'bar'}, secret, {expiresIn: {a:1}});
    }).toThrow(/"expiresIn" should be a number of seconds or string/);
    expect(() => {
      jwt.sign({foo:'bar'}, secret, {audience: 123});
    }).toThrow(/"audience" must be a string or array/);
  });

  it('throws error if mutating payload', () => {
    const payload = { a: 1 };
    const copy = { ...payload };
    jwt.sign(payload, secret, { mutatePayload: true }, (err, token) => {
      expect(token).toBeDefined();
      expect(payload).not.toEqual(copy); // mutated
    });
  });

  it('verifies using RS256 async/invalid key', done => {
    const privateKey = fs.readFileSync(path.join(__dirname, 'rsa-private.pem'));
    const wrongPubKey = fs.readFileSync(path.join(__dirname, 'ecdsa-public-invalid.pem'));
    jwt.sign({test: 'val'}, privateKey, {algorithm: 'RS256'}, (err, token) => {
      expect(err).toBeNull();
      jwt.verify(token, wrongPubKey, {algorithms: ['RS256']}, (e, decoded) => {
        expect(e).not.toBeNull();
        done();
      });
    });
  });

  it('verify errors: missing jwt, not string, malformed, decode error, invalid algo', () => {
    expect(() => jwt.verify()).toThrow(/jwt must be provided/);
    expect(() => jwt.verify(123)).toThrow(/jwt must be a string/);
    expect(() => jwt.verify('a.b')).toThrow(/jwt malformed/);
    expect(() => jwt.verify('eyJhbGciOiJIUzI1NiJ9.e30=.xxxx', secret, {algorithms: ['none']})).toThrow();
  });

  it('verify errors: clockTimestamp, nonce, allowInvalidAsymmetricKeyTypes wrong type', () => {
    expect(() => jwt.verify('a.b.c', secret, { clockTimestamp: 'not-a-number' })).toThrow(/clockTimestamp must be a number/);
    expect(() => jwt.verify('a.b.c', secret, { nonce: 123 })).toThrow(/nonce must be a non-empty string/);
    expect(() => jwt.verify('a.b.c', secret, { allowInvalidAsymmetricKeyTypes: 'yes' })).toThrow(/allowInvalidAsymmetricKeyTypes must be a boolean/);
  });

  it('unsigned tokens: no signature, no algorithms, but secret provided', done => {
    jwt.sign({foo:'bar'}, secret, { algorithm: 'none' }, (err, token) => {
      expect(err).toBeNull();
      // Remove signature part
      const unsigned = token.split('.').slice(0,2).join('.') + '.';
      jwt.verify(unsigned, '', {algorithms: ['none']}, (e, dec) => {
        expect(e).toBeNull();
        expect(dec.foo).toBe('bar');
        done();
      });
    });
  });

  it('verify errors: signature required, secret missing, invalid key material', () => {
    // Token with signature but missing secret
    const payload = {foo: 'bar'};
    jwt.sign(payload, secret, {}, (err, token) => {
      expect(err).toBeNull();
      expect(() => jwt.verify(token)).toThrow(/secret or public key must be provided/);
    });

    // Bad key material
    const token = [
      Buffer.from(JSON.stringify({alg:"HS256", typ:"JWT"})).toString('base64').replace(/=/g, ''),
      Buffer.from(JSON.stringify({foo:"bar"})).toString('base64').replace(/=/g,''),
      Buffer.from('sig').toString('base64').replace(/=/g,'')
    ].join('.');

    expect(() => jwt.verify(token, {})).toThrow(/secretOrPublicKey is not valid key material/);
  });
});