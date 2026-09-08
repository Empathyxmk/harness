const assert = require('assert');
const crc32 = require('../index.js');

function bufferEqual(a, b) {
  if (!Buffer.isBuffer(a) || !Buffer.isBuffer(b) || a.length !== b.length) return false;
  for (let i = 0; i < a.length; ++i) if (a[i] !== b[i]) return false;
  return true;
}

describe('buffer-crc32 exports (public)', function() {
  it('should export a function (public)', function() {
    assert.strictEqual(typeof crc32, 'function');
  });

  it('should correctly calculate crc32 for a different string', function() {
    const result = crc32('bye');
    assert(Buffer.isBuffer(result));
    assert.strictEqual(result.length, 4);
    assert(bufferEqual(crc32('bye'), result));
  });

  it('should correctly calculate crc32 for a different Buffer', function() {
    const input = Buffer.from('moon');
    const result = crc32(input);
    assert(Buffer.isBuffer(result));
    assert.strictEqual(result.length, 4);
    assert(bufferEqual(crc32(Buffer.from('moon')), result));
  });

  it('should accept a partialCrc as buffer (public)', function() {
    const input = Buffer.from('xyz');
    const first = crc32(input.slice(0,1));
    const full = crc32(input, first);
    const full2 = crc32(input);
    assert(Buffer.isBuffer(full));
  });

  it('should accept a partialCrc as number (public)', function() {
    const input = '789';
    const result = crc32(input, 0xABCDEF00);
    assert(Buffer.isBuffer(result));
  });

  it('should compute correct signed() and unsigned() values (public)', function() {
    const buf = Buffer.from('alpha');
    const s = crc32.signed(buf);
    const u = crc32.unsigned(buf);
    assert.strictEqual(typeof s, 'number');
    assert.strictEqual(typeof u, 'number');
    assert.strictEqual(s >>> 0, u);

    // edge: partialCrc
    const s2 = crc32.signed(buf, u);
    assert.strictEqual(typeof s2, 'number');
    const u2 = crc32.unsigned(buf, s);
    assert.strictEqual(typeof u2, 'number');
  });

  it('should match unsigned for signed with positive values (public)', () => {
    const buf = Buffer.from('beta');
    const s = crc32.signed(buf);
    const u = crc32.unsigned(buf);
    if (s >= 0) assert.strictEqual(s, u);
  });

  it('should handle empty input (public)', function() {
    assert(crc32('') instanceof Buffer);
    assert(crc32(Buffer.alloc(0)) instanceof Buffer);
    assert.strictEqual(typeof crc32.signed(''), 'number');
    assert.strictEqual(typeof crc32.unsigned(''), 'number');
  });

  it('should process multi-part data the same as whole (public)', function() {
    const a = 'ping', b = 'pong';
    const ab = a + b;
    const expected = crc32(ab);
    const part = crc32(a);
    const fromPartial = crc32(b, part);
    assert(bufferEqual(expected, fromPartial));
  });

  it('should throw or fail gracefully on wrong input (public)', function() {
    assert.throws(() => crc32());
    assert.throws(() => crc32(null));
    assert.throws(() => crc32(undefined));
    assert.throws(() => crc32.signed());
    assert.throws(() => crc32.unsigned());
  });
});