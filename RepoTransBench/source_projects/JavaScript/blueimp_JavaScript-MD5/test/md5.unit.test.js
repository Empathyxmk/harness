// Test suite for blueimp-md5 via the CJS shim
const { expect } = require('chai');
const md5 = require('../js/md5.cjs.js');

describe('MD5 hash function', function () {
  it('should hash empty string', function () {
    expect(md5('')).to.equal('d41d8cd98f00b204e9800998ecf8427e');
  });

  it('should hash short ASCII', function () {
    expect(md5('abc')).to.equal('900150983cd24fb0d6963f7d28e17f72');
  });

  it('should hash long input', function () {
    expect(md5('The quick brown fox jumps over the lazy dog')).to.equal('9e107d9d372bb6826bd81d3542a419d6');
  });

  it('should hash with key (hmac)', function () {
    // The correct HMAC-MD5 of 'abc' with key 'key' per blueimp implementation is:
    expect(md5('abc', 'key')).to.equal('ffb7c0fc166f7ca075dfa04d59aed232');
  });

  it('should hash numbers as string', function () {
    expect(md5(123)).to.equal(md5('123'));
  });

  it('should hash boolean false as string', function () {
    expect(md5(false)).to.equal(md5('false'));
  });

  it('should hash boolean true as string', function () {
    expect(md5(true)).to.equal(md5('true'));
  });

  it('should hash null as string', function () {
    expect(md5(null)).to.equal(md5('null'));
  });

  it('should hash undefined as string', function () {
    expect(md5(undefined)).to.equal(md5('undefined'));
  });

  it('should produce raw output when third param true', function () {
    const hash = md5('blueimp', null, true);
    expect(hash).to.be.a('string');
    expect(hash.length).to.equal(16);
  });

  it('should handle multibyte (emoji)', function () {
    expect(md5('😀')).to.be.a('string');
  });

  it('should handle empty key for HMAC as equivalent to no key', function () {
    expect(md5('abc', '')).to.equal(md5('abc'));
  });

  it('should produce different results with key', function () {
    expect(md5('abc', 'key')).to.not.equal(md5('abc'));
  });

  it('should not throw for object input', function () {
    expect(() => md5({foo:'bar'})).to.not.throw();
  });

  it('should hash buffer (Node.js Buffer shim)', function () {
    const buf = Buffer.from('abc');
    expect(md5(buf)).to.equal('900150983cd24fb0d6963f7d28e17f72');
  });
});

describe('MD5 edge and error handling', function () {
  it('should output hex when raw is false', function () {
    const out = md5('abc', null, false);
    expect(out).to.match(/^[\da-f]{32}$/);
  });

  it('should output raw when raw===1', function () {
    const raw = md5('abc', null, 1);
    expect(raw).to.be.a('string');
    expect(raw.length).to.equal(16); // 16 bytes raw
  });

  it('should treat undefined raw param as hex', function () {
    const out = md5('abc', null, undefined);
    expect(out).to.match(/^[\da-f]{32}$/);
  });

  it('should treat key with non-string', function () {
    expect(md5('abc', {k:1})).to.be.a('string');
  });

  it('should hash with key and produce 16 byte output in raw', function () {
    const raw = md5('abc', 'key', true);
    expect(raw.length).to.equal(16);
  });
});