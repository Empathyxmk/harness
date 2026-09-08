// Public test suite for blueimp-md5 via the CJS shim - different test data!
const { expect } = require('chai');
const md5 = require('../js/md5.cjs.js');

describe('MD5 hash function (public tests)', function () {
  it('should hash a single space', function () {
    expect(md5(' ')).to.equal('7215ee9c7d9dc229d2921a40e899ec5f');
  });

  it('should hash different ASCII', function () {
    expect(md5('def')).to.equal('4ed9407630eb1000c0f6b63842defa7d');
  });

  it('should hash a pangram without spaces', function () {
    expect(md5('thequickbrownfoxjumpsoverthelazydog')).to.equal('5c6ffbdd40d9556b73a21e63c3e0e904');
  });

  it('should hash with a different key (hmac)', function () {
    // The HMAC-MD5 of 'hello' with key 'world'
    expect(md5('hello', 'world')).to.equal('fa4eeaeb4ec9f72b26e17e30ee466c03');
  });

  it('should hash other number as string', function () {
    expect(md5(456)).to.equal(md5('456'));
  });

  it('should hash boolean true as string (repeat for public)', function () {
    expect(md5(true)).to.equal(md5('true'));
  });

  it('should hash boolean false as string (repeat for public)', function () {
    expect(md5(false)).to.equal(md5('false'));
  });

  it('should hash NaN as string', function () {
    expect(md5(NaN)).to.equal(md5('NaN'));
  });

  it('should hash null as string (repeat for public)', function () {
    expect(md5(null)).to.equal(md5('null'));
  });

  it('should hash an array as string', function () {
    expect(() => md5([1,2,3])).to.not.throw();
  });

  it('should produce raw output (third param true) of correct length (other input)', function () {
    const hash = md5('publicTest', null, true);
    expect(hash).to.be.a('string');
    expect(hash.length).to.equal(16);
  });

  it('should handle multibyte (CJK)', function () {
    expect(md5('漢字')).to.be.a('string');
  });

  it('should handle empty key for HMAC as equivalent to no key (different input)', function () {
    expect(md5('def', '')).to.equal(md5('def'));
  });

  it('should produce different results with key (public input)', function () {
    expect(md5('def', 'differentKey')).to.not.equal(md5('def'));
  });

  it('should not throw for Date input', function () {
    expect(() => md5(new Date())).to.not.throw();
  });

  it('should hash buffer with different content (Node.js Buffer shim)', function () {
    const buf = Buffer.from('test');
    expect(md5(buf)).to.equal('098f6bcd4621d373cade4e832627b4f6');
  });
});

describe('MD5 edge and error handling (public)', function () {
  it('should output hex when raw is false (different input)', function () {
    const out = md5('blue', null, false);
    expect(out).to.match(/^[\da-f]{32}$/);
  });

  it('should output raw when raw===1 (public input)', function () {
    const raw = md5('another', null, 1);
    expect(raw).to.be.a('string');
    expect(raw.length).to.equal(16); // 16 bytes raw
  });

  it('should treat undefined raw param as hex (public input)', function () {
    const out = md5('different', null, undefined);
    expect(out).to.match(/^[\da-f]{32}$/);
  });

  it('should treat key as number', function () {
    expect(md5('def', 42)).to.be.a('string');
  });

  it('should hash with key and produce 16 byte output in raw (public)', function () {
    const raw = md5('world', 'hello', true);
    expect(raw.length).to.equal(16);
  });
});