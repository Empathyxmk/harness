const { parse } = require('../parse');

function objResult(result) {
  // Returns only key:value pairs from parse output, ignoring comments/non-envs
  if (Array.isArray(result)) {
    const dict = {};
    for (const item of result) {
      if (item.isEnvVar) dict[item.key] = item.value;
    }
    return dict;
  }
  return result;
}

describe('parse (public)', () => {
  it('should parse a simple key-value string with different key', () => {
    const result = objResult(parse('BAR=foo'));
    expect(result).toEqual({ BAR: 'foo' });
  });

  it('should parse multiple lines with different keys/values', () => {
    const result = objResult(parse('X=100\nY=200'));
    expect(result).toEqual({ X: '100', Y: '200' });
  });

  it('should trim whitespace for other keys and values', () => {
    const result = objResult(parse('  HELLO =  world  '));
    expect(result).toEqual({ HELLO: 'world  ' });
  });

  it('should ignore comments (different comment text)', () => {
    const result = parse('# This is a comment\nBAR=foo\n# Another comment');
    expect(result).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ key: 'BAR', value: 'foo', isEnvVar: true }),
      ])
    );
  });

  it('should handle empty lines for different keys', () => {
    const result = parse('\nFOO1=abc\n\nFOO2=xyz\n');
    expect(result).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ key: 'FOO1', value: 'abc', isEnvVar: true }),
        expect.objectContaining({ key: 'FOO2', value: 'xyz', isEnvVar: true }),
      ])
    );
  });

  it('should ignore lines without = (different keys)', () => {
    const result = parse('ONE=11\nNO_PAIR\nTWO=22');
    expect(result.filter(x => x.isEnvVar)).toEqual([
      expect.objectContaining({ key: 'ONE', value: '11', isEnvVar: true }),
      expect.objectContaining({ key: 'TWO', value: '22', isEnvVar: true }),
    ]);
  });

  it('should parse quoted strings (different values)', () => {
    expect(objResult(parse('GREETING="hello world"'))).toEqual({ GREETING: 'hello world' });
  });

  it('should handle = within quoted values (different value)', () => {
    expect(objResult(parse('EQUAL="foo=bar"'))).toEqual({ EQUAL: 'foo=bar' });
  });

  it('should return {} or empty for whitespace input', () => {
    const result = parse(' ');
    if (Array.isArray(result) && result.length === 1 && result[0].isEnvVar === false) {
      expect(result[0].value).toBe('');
    } else {
      expect(result).toEqual({});
    }
  });

  // Buffer input with new values
  it('should handle buffer input with different data', () => {
    const str = Buffer.from('ALPHA=OMEGA\nOMEGA=ALPHA');
    const result = objResult(parse(str));
    expect(result).toEqual({ ALPHA: 'OMEGA', OMEGA: 'ALPHA' });
  });

  it('should handle single quoted strings (different key/value)', () => {
    expect(objResult(parse("KEY='single quoted'"))).toEqual({ KEY: 'single quoted' });
  });

  it('should handle empty value for another key', () => {
    expect(objResult(parse('BAR='))).toEqual({ BAR: '' });
  });

  it('should process whitespace-only lines with tabs', () => {
    const result = parse('\t \n\t');
    expect(result.every(x => x.isEnvVar === false)).toBe(true);
  });

  it('should parse value with # in it if quoted, for another key', () => {
    expect(objResult(parse('BAR="#hashInValue"'))).toEqual({ BAR: '#hashInValue' });
  });

  it('should ignore content after # at the end of lines when not quoted, for another key', () => {
    const parsed = parse('BAR=baz # end comment');
    expect(parsed[0]).toEqual(expect.objectContaining({ key: 'BAR', value: 'baz ', isEnvVar: true }));
  });

  it('should return isEnvVar: false for just a comment, with different comment', () => {
    const parsed = parse('# nothing here');
    expect(parsed[0].isEnvVar).toBe(false);
    expect(parsed[0].key).toBe(null);
  });

  it('should parse keys with periods and dashes (different keys)', () => {
    const out = parse('X.Y=42\nX-Y=42');
    expect(out.filter(x => x.isEnvVar).map(x => x.key)).toEqual(['X.Y', 'X-Y']);
  });

  it('should parse empty values with and without quotes for public keys', () => {
    const out1 = parse('EMPTY1=');
    const out2 = parse('EMPTY2=""');
    const out3 = parse("EMPTY3=''");
    expect(objResult(out1)).toEqual({ EMPTY1: '' });
    expect(objResult(out2)).toEqual({ EMPTY2: '' });
    expect(objResult(out3)).toEqual({ EMPTY3: '' });
  });

  it('should return isEnvVar: false for a malformed public line', () => {
    const out = parse('=no_key');
    expect(out[0].isEnvVar).toBe(false);
    expect(out[0].key).toBe(null);
    expect(typeof out[0].value).toBe('string');
  });
});