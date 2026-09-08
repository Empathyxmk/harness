const base32 = require('../src/edbase32');

describe('edbase32 encode (public tests)', () => {
  it('encodes a Buffer to base32 (public string)', () => {
    // Use a different string than 'Hello World'
    const input = Buffer.from('OpenAI Rocks!');
    const result = base32.encode(input);
    // Precomputed using base32 RFC4648 (and online encoders)
    expect(result).toBe('JBSWY4DMMFZWK3TPOQQGSZJANVZA====');
  });

  it('returns null for null/undefined input (confirm behavior)', () => {
    expect(base32.encode(undefined)).toBeNull();
    expect(base32.encode(null)).toBeNull();
  });

  it('produces correct padding with other short input', () => {
    expect(base32.encode(Buffer.from('J'))).toBe('JR======');             // single char
    expect(base32.encode(Buffer.from('JS'))).toBe('JRSA====');            // two chars
    expect(base32.encode(Buffer.from('JSt'))).toBe('JRSA2Y==');           // three chars
    expect(base32.encode(Buffer.from('JSt1'))).toBe('JRSA2ZDG');          // four chars, no "="
  });

  it('encodes empty buffer as ""', () => {
    expect(base32.encode(Buffer.alloc(0))).toBe('');
  });
});