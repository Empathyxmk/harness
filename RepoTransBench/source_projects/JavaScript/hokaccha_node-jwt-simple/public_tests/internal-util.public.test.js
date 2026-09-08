const jwt = require('../lib/jwt');
const expect = require('expect.js');

// "Internals" test: base64url functionality, assignProperties, error edges

describe('jwt internal utilities (public)', function() {
  it('base64urlEncode/base64urlDecode roundtrip for unicode', function() {
    const str = 'ünicødé!$#@';
    const enc = jwt.__test__.base64urlEncode(str);
    const dec = jwt.__test__.base64urlDecode(enc);
    expect(dec).to.equal(str);
  });

  it('base64urlUnescape with different strange input', function() {
    // The output will have padding according to the implementation
    const input = '_-_fooBar';
    const output = jwt.__test__.base64urlUnescape(input);
    expect(output).to.match(/^[-+_]fooBar\/=*$/); // allow for variety of special chars and padding
  });

  it('assignProperties only copies direct (not inherited) properties', function() {
    function Source() {
      this.x = 47;
    }
    Source.prototype.protoProp = 99;
    const src = new Source();
    const dest = {z: 31};
    jwt.__test__.assignProperties(dest, src);
    expect(dest).to.have.property('x',47);
    expect(dest).to.not.have.property('protoProp');
    expect(dest).to.have.property('z',31);
  });

  it('sign with another unknown type throws error', function() {
    expect(() => jwt.__test__.sign('q','p','sha384','unknown-alg')).to.throwError();
  });

  it('verify with another unknown type returns false', function() {
    expect(jwt.__test__.verify('q','p','sha384','unknown-alg','someSig')).to.be(false);
  });
});

// Cover error branch for invalid JSON during decode
describe('jwt.decode error edge (public)', function() {
  it('throws error on different invalid header JSON', function() {
    const token = [Buffer.from('{:wrong}').toString('base64'), Buffer.from('{"x":7}').toString('base64'), 'segsig'].join('.');
    expect(() => jwt.decode(token, 'otherkey')).to.throwError();
  });

  it('throws error on different invalid payload JSON', function() {
    const token = [Buffer.from('{"alg":"HS384"}').toString('base64'), Buffer.from('not-real-json').toString('base64'), 'difsig'].join('.');
    expect(() => jwt.decode(token, 'otherkey')).to.throwError();
  });
});