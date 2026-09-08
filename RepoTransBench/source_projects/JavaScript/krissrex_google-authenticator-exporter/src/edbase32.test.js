const base32 = require('./edbase32');

describe('edbase32 encode', () => {
  it('encodes a Buffer to base32 (hello world)', () => {
    const input = Buffer.from('Hello World');
    const result = base32.encode(input);
    // Matches Google's implementation/rfc4648
    expect(result).toBe('JBSWY3DPEBLW64TMMQ======');
  });

  it('returns null for null/undefined input', () => {
    expect(base32.encode(undefined)).toBeNull();
    expect(base32.encode(null)).toBeNull();
  });

  it('produces correct padding with short input', () => {
    expect(base32.encode(Buffer.from('M'))).toBe('JU======');
    expect(base32.encode(Buffer.from('Ma'))).toBe('JVQQ====');
    expect(base32.encode(Buffer.from('Man'))).toBe('JVQW4===');
    // Actual implementation produces 'JVQW4MI=' for 'Man1'
    expect(base32.encode(Buffer.from('Man1'))).toBe('JVQW4MI=');
  });

  it('encodes empty buffer as ""', () => {
    expect(base32.encode(Buffer.alloc(0))).toBe('');
  });
});