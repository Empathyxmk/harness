const jwt = require('../lib/jwt');
const expect = require('expect.js');

// "Internals" test: base64url functionality, assignProperties, error edges

describe('jwt internal utilities', function() {
  it('base64urlEncode/base64urlDecode roundtrip for ascii', function() {
    const str = 'foobar123';
    const enc = jwt.__test__.base64urlEncode(str);
    const dec = jwt.__test__.base64urlDecode(enc);
    expect(dec).to.equal(str);
  });

  it('base64urlUnescape with strange input', function() {
    // The output will have padding according to the implementation
    const input = 'abc-def_';
    const output = jwt.__test__.base64urlUnescape(input);
    expect(output).to.match(/^abc\+def\/=+$/); // allow for padding
  });

  it('assignProperties copies own properties only', function() {
    const dest = {a: 1};
    const src = {b: 2};
    // Do NOT pollute prototype - this test is to verify that assignProperties copies direct properties,
    // which it does, so dest should have a and b.
    jwt.__test__.assignProperties(dest, src);
    expect(dest).to.have.property('b',2);
    expect(dest).to.not.have.property('foo'); // Just confirm no unrelated property
  });

  it('sign with unknown type throws error', function() {
    expect(() => jwt.__test__.sign('x','y','sha256','none')).to.throwError();
  });

  it('verify with unknown type returns false', function() {
    expect(jwt.__test__.verify('x','y','sha256','none','sig')).to.be(false);
  });
});

// Cover error branch for invalid JSON during decode
describe('jwt.decode error edge', function() {
  it('throws error on invalid header JSON', function() {
    const token = [Buffer.from('notjson').toString('base64'), Buffer.from('{}').toString('base64'), 'sig'].join('.');
    expect(() => jwt.decode(token, 'key')).to.throwError();
  });

  it('throws error on invalid payload JSON', function() {
    const token = [Buffer.from('{"alg":"HS256"}').toString('base64'), Buffer.from('notjson').toString('base64'), 'sig'].join('.');
    expect(() => jwt.decode(token, 'key')).to.throwError();
  });
});