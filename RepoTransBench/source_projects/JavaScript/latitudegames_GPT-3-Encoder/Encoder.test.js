const { encode, decode } = require('./Encoder');

describe('GPT-3 Encoder - main functionality', () => {
  it('empty string', () => {
    const encoded = encode('');
    expect(Array.isArray(encoded)).toBeTruthy();
    expect(encoded.length).toBe(0);
    expect(decode(encoded)).toBe('');
  });

  it('space', () => {
    const encoded = encode(' ');
    expect(decode(encoded)).toBe(' ');
  });

  it('tab', () => {
    const encoded = encode('\t');
    expect(decode(encoded)).toBe('\t');
  });

  it('simple text', () => {
    const text = 'hello world';
    const encoded = encode(text);
    expect(Array.isArray(encoded)).toBeTruthy();
    expect(encoded.length).toBeGreaterThan(0);
    const decoded = decode(encoded);
    expect(decoded).toBe(text);
  });

  it('multi-token word', () => {
    // likely to be split
    const text = 'indivisibility';
    const encoded = encode(text);
    expect(Array.isArray(encoded)).toBeTruthy();
    expect(decode(encoded)).toBe(text);
  });

  it('emojis', () => {
    const text = '😀😃😄😁';
    const encoded = encode(text);
    expect(Array.isArray(encoded)).toBeTruthy();
    expect(decode(encoded)).toBe(text);
  });

  it('properties of Object', () => {
    // ensure decoder/encoder properties don't break due to prototype pollution
    Object.prototype.bad = true;
    const text = 'danger';
    const encoded = encode(text);
    expect(decode(encoded)).toBe(text);
    delete Object.prototype.bad;
  });

  it('special unicode in input', () => {
    const text = '\u00a9\u2202\u2603';
    const encoded = encode(text);
    expect(decode(encoded)).toBe(text);
  });

  it('long sentence', () => {
    const long = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin viverra, ligula sit amet ultrices semper, ligula arcu tristique sapien, a accumsan nisi mauris ac eros.';
    const encoded = encode(long);
    expect(decode(encoded)).toBe(long);
  });

  it('all bytes in unicode range 0-255', () => {
    // Test all possible byte values round-trip
    const text = Array.from({length:256},(v,i)=>String.fromCharCode(i)).join('');
    const encoded = encode(text);
    expect(decode(encoded)).toBe(text);
  });
});

describe('Encoder.js edge-case/branch coverage', () => {
  it('decodes empty array', () => {
    expect(decode([])).toBe('');
  });

  it('decode/encode is reversible for various lengths', () => {
    for (const str of ['a', 'ab', 'abc', 'abcd', 'abcde']) {
      expect(decode(encode(str))).toBe(str);
    }
  });

  it('does not mutate the input tokens array', () => {
    const text = 'mutable test';
    const encoded = encode(text);
    const original = [...encoded];
    decode(encoded);
    expect(encoded).toEqual(original);
  });
});