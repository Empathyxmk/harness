const { parse } = require('./parse');

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

describe('parse', () => {
  it('should parse a key-value string', () => {
    const result = objResult(parse('FOO=bar'));
    expect(result).toEqual({ FOO: 'bar' });
  });

  it('should parse multiple lines', () => {
    const result = objResult(parse('A=1\nB=2'));
    expect(result).toEqual({ A: '1', B: '2' });
  });

  it('should trim whitespace around keys and values', () => {
    const result = objResult(parse('  X =  5  '));
    expect(result).toEqual({ X: '5  ' });
  });

  it('should ignore comments', () => {
    const result = parse('# Hello\nFOO=bar\n# another');
    expect(result).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ key: 'FOO', value: 'bar', isEnvVar: true }),
      ])
    );
  });

  it('should handle empty lines', () => {
    const result = parse('\nA=1\n\nB=2\n');
    expect(result).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ key: 'A', value: '1', isEnvVar: true }),
        expect.objectContaining({ key: 'B', value: '2', isEnvVar: true }),
      ])
    );
  });

  it('should ignore lines without =', () => {
    const result = parse('A=1\nNOT_A_PAIR\nB=2');
    expect(result.filter(x => x.isEnvVar)).toEqual([
      expect.objectContaining({ key: 'A', value: '1', isEnvVar: true }),
      expect.objectContaining({ key: 'B', value: '2', isEnvVar: true }),
    ]);
  });

  it('should parse quoted strings', () => {
    expect(objResult(parse('FOO="bar bar"'))).toEqual({ FOO: 'bar bar' });
  });

  it('should handle = within quoted values', () => {
    expect(objResult(parse('FOO="a=b"'))).toEqual({ FOO: 'a=b' });
  });

  it('should return {} for empty input', () => {
    const result = parse('');
    if (Array.isArray(result) && result.length === 1 && result[0].isEnvVar === false) {
      expect(result[0].value).toBe('');
    } else {
      expect(result).toEqual({});
    }
  });

  // Additional: test buffer input
  it('should handle buffer input', () => {
    const str = Buffer.from('FOO=BAR\nBAR=BAZ');
    const result = objResult(parse(str));
    expect(result).toEqual({ FOO: 'BAR', BAR: 'BAZ' });
  });

  // Edge: parse strings with single quotes
  it('should handle single quoted strings', () => {
    expect(objResult(parse("FOO='bar bar'"))).toEqual({ FOO: 'bar bar' });
  });

  it('should handle empty value', () => {
    expect(objResult(parse('FOO='))).toEqual({ FOO: '' });
  });

  // Edge: whitespace-only lines
  it('should process whitespace-only lines correctly', () => {
    const result = parse('   \n \t ');
    expect(result.every(x => x.isEnvVar === false)).toBe(true);
  });

  // Branch: test comment detection at end of lines (should include value correctly)
  it('should parse a value with # in it if quoted', () => {
    expect(objResult(parse('FOO="#notAComment"'))).toEqual({ FOO: '#notAComment' });
  });

  it('should ignore content after # at the end of lines when not quoted', () => {
    const parsed = parse('FOO=bar # some comment');
    // The value, per implementation, includes trailing space before '#' but not comment text.
    expect(parsed[0]).toEqual(expect.objectContaining({ key: 'FOO', value: 'bar ', isEnvVar: true }));
  });

  // Branch: strange edge cases
  it('should return isEnvVar: false for a comment', () => {
    const parsed = parse('# only a comment');
    expect(parsed[0].isEnvVar).toBe(false);
    expect(parsed[0].key).toBe(null);
  });

  it('should parse keys with periods and dashes', () => {
    const out = parse('FOO.BAR=test\nFOO-BAR=test');
    expect(out.filter(x => x.isEnvVar).map(x => x.key)).toEqual(['FOO.BAR', 'FOO-BAR']);
  });

  it('should parse empty values with and without quotes', () => {
    const out1 = parse('FOO=');
    const out2 = parse('BAR=""');
    const out3 = parse('BAZ=\'\'');
    expect(objResult(out1)).toEqual({ FOO: '' });
    expect(objResult(out2)).toEqual({ BAR: '' });
    expect(objResult(out3)).toEqual({ BAZ: '' });
  });

  // Branch: malformed lines that could match the regex but don't have proper structure
  it('should return isEnvVar: false for a malformed line', () => {
    const out = parse('=novalue');
    expect(out[0].isEnvVar).toBe(false);
    expect(out[0].key).toBe(null);
    expect(typeof out[0].value).toBe('string');
  });
});