const { generateEnvTypes } = require('../gen-env-types');

describe('generateEnvTypes (public)', () => {
  it('should generate env types for different keys', () => {
    const input = 'USER=alex\nPASSWORD=secret';
    const out = generateEnvTypes(input);
    expect(out).toContain('declare namespace NodeJS');
    expect(out).toContain('USER: string;');
    expect(out).toContain('PASSWORD: string;');
  });

  it('should work with a different single key', () => {
    const input = 'BAR=baz';
    const out = generateEnvTypes(input);
    expect(out).toContain('BAR: string;');
    expect(out).toMatch(/declare namespace NodeJS/);
  });

  it('should return a valid TS declaration if whitespace only', () => {
    const out = generateEnvTypes('   ');
    expect(out).toContain('declare namespace NodeJS');
    expect(out).toContain('interface ProcessEnv');
  });

  it('should handle keys with different underscores/numbers', () => {
    const out = generateEnvTypes('NAME_2=john\nA3=test');
    expect(out).toContain('NAME_2: string;');
    expect(out).toContain('A3: string;');
  });

  it('should ignore different comment lines', () => {
    const out = generateEnvTypes('# First comment\nHELLO=world\n# another comment\nWORLD=hello');
    expect(out).toContain('HELLO: string;');
    expect(out).toContain('WORLD: string;');
    expect(out).not.toContain('#');
  });

  it('should not include lines without key (different non-pair line)', () => {
    const out = generateEnvTypes('ONE=one\nmissingpair\nTWO=two');
    expect(out).toContain('ONE: string;');
    expect(out).toContain('TWO: string;');
    expect(out).not.toContain('missingpair');
  });

  it('should support keys with only a value for different key', () => {
    const out = generateEnvTypes('BLANK=');
    expect(out).toContain('BLANK: string;');
  });

  it('should handle keys with dashes or spaces (should skip or sanitize) for public data', () => {
    const out = generateEnvTypes('NICE_KEY=good\nBAD-KEY=bad\nKEY WITH SPACE=fail2');
    expect(out).toContain('NICE_KEY: string;');
    expect(out).not.toContain('BAD-KEY: string;');
    expect(out).not.toContain('KEY WITH SPACE: string;');
  });

  it('should only include each env key once for public values', () => {
    const out = generateEnvTypes('FOO=abc\nFOO=def\nBAR=xyz');
    expect((out.match(/FOO: string;/g) || []).length).toBe(1);
    expect((out.match(/BAR: string;/g) || []).length).toBe(1);
  });

  it('should skip lines where the key is not a valid identifier, for public keys', () => {
    const out = generateEnvTypes('2BAD=shouldskip\n_2GOOD=shouldwork');
    expect(out).not.toContain('2BAD:');
    expect(out).toContain('_2GOOD: string;');
  });

  it('should skip keys that start with a number (public case)', () => {
    const out = generateEnvTypes('99KEY=notype\nTYPE99=has');
    expect(out).not.toContain('99KEY:');
    expect(out).toContain('TYPE99: string;');
  });

  it('should not include keys with invalid characters (different keys)', () => {
    const out = generateEnvTypes('JUST-KEY=skip\nANOTHER KEY=skip\nDOT.KEY=skip');
    expect(out).not.toContain('JUST-KEY:');
    expect(out).not.toContain('ANOTHER KEY:');
    expect(out).not.toContain('DOT.KEY:');
  });
});