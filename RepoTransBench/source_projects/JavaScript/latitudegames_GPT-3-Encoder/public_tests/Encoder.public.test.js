const { encode, decode } = require('../Encoder');

describe('GPT-3 Encoder - main functionality (public)', () => {
  it('single character', () => {
    const encoded = encode('x');
    expect(Array.isArray(encoded)).toBeTruthy();
    expect(encoded.length).toBe(1);
    expect(decode(encoded)).toBe('x');
  });

  it('newline', () => {
    const encoded = encode('\n');
    expect(decode(encoded)).toBe('\n');
  });

  it('carriage return', () => {
    const encoded = encode('\r');
    expect(decode(encoded)).toBe('\r');
  });

  it('different simple text', () => {
    const text = 'test string';
    const encoded = encode(text);
    expect(Array.isArray(encoded)).toBeTruthy();
    expect(encoded.length).toBeGreaterThan(0);
    const decoded = decode(encoded);
    expect(decoded).toBe(text);
  });

  it('another multi-token word', () => {
    // likely to be split
    const text = 'unbelievability';
    const encoded = encode(text);
    expect(Array.isArray(encoded)).toBeTruthy();
    expect(decode(encoded)).toBe(text);
  });

  it('different emojis', () => {
    const text = '😎🤓🧐🥸';
    const encoded = encode(text);
    expect(Array.isArray(encoded)).toBeTruthy();
    expect(decode(encoded)).toBe(text);
  });

  it('properties of Array prototype', () => {
    // ensure decoder/encoder properties don't break due to prototype pollution
    Array.prototype.bad = true;
    const text = 'hazard';
    const encoded = encode(text);
    expect(decode(encoded)).toBe(text);
    delete Array.prototype.bad;
  });

  it('other special unicode in input', () => {
    const text = '\u263A\u265E\u2665'; // ☺♞♥
    const encoded = encode(text);
    expect(decode(encoded)).toBe(text);
  });

  it('another long sentence', () => {
    const long = 'Quick brown fox jumps over the lazy dog, testing encoding with varied characters... Wow!';
    const encoded = encode(long);
    expect(decode(encoded)).toBe(long);
  });

  it('all printable ASCII chars (32-126)', () => {
    // Test all printable ASCII chars round-trip
    const text = Array.from({length:95},(v,i)=>String.fromCharCode(i+32)).join('');
    const encoded = encode(text);
    expect(decode(encoded)).toBe(text);
  });
});

describe('Encoder.js edge-case/branch coverage (public)', () => {
  it('decodes array with no elements', () => {
    expect(decode([])).toBe('');
  });

  it('decode/encode is reversible for various different strings', () => {
    for (const str of ['z', 'yz', 'wxyz', 'mnop', 'qrstu']) {
      expect(decode(encode(str))).toBe(str);
    }
  });

  it('does not mutate the input tokens array for different text', () => {
    const text = 'immutability check';
    const encoded = encode(text);
    const original = [...encoded];
    decode(encoded);
    expect(encoded).toEqual(original);
  });
});