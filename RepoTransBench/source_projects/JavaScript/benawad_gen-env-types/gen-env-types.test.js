const { generateEnvTypes } = require('./gen-env-types');

describe('generateEnvTypes', () => {
  it('should generate env types for keys', () => {
    const input = 'A=1\nB=2';
    const out = generateEnvTypes(input);
    expect(out).toContain('declare namespace NodeJS');
    expect(out).toContain('A: string;');
    expect(out).toContain('B: string;');
  });

  it('should work with single key', () => {
    const input = 'FOO=bar';
    const out = generateEnvTypes(input);
    expect(out).toContain('FOO: string;');
    expect(out).toMatch(/declare namespace NodeJS/);
  });

  it('should return a valid TS declaration if empty', () => {
    const out = generateEnvTypes('');
    expect(out).toContain('declare namespace NodeJS');
    expect(out).toContain('interface ProcessEnv');
  });

  it('should handle keys with numbers and underscores', () => {
    const out = generateEnvTypes('FOO_1=hello\nB2=foo');
    expect(out).toContain('FOO_1: string;');
    expect(out).toContain('B2: string;');
  });

  it('should ignore comment lines', () => {
    const out = generateEnvTypes('# Hello\nFOO=1\n# again\nBAR=2');
    expect(out).toContain('FOO: string;');
    expect(out).toContain('BAR: string;');
    expect(out).not.toContain('#');
  });

  it('should not include lines without key', () => {
    const out = generateEnvTypes('FOO=bar\nnotapair\nBAR=baz');
    expect(out).toContain('FOO: string;');
    expect(out).toContain('BAR: string;');
    expect(out).not.toContain('notapair');
  });

  it('should support keys with only a value', () => {
    const out = generateEnvTypes('EMPTY=');
    expect(out).toContain('EMPTY: string;');
  });

  // Edge case: keys with strange names (should sanitize or throw)
  it('should handle keys with dashes or spaces (should skip or sanitize)', () => {
    const out = generateEnvTypes('GOOD_KEY=ok\nBAD-KEY=bad\nKEY WITH SPACE=fail');
    expect(out).toContain('GOOD_KEY: string;');
    // These should not appear as TS properties (invalid symbols)
    expect(out).not.toContain('BAD-KEY: string;');
    expect(out).not.toContain('KEY WITH SPACE: string;');
  });

  // Branch: what happens with duplicate keys?
  it('should only include each env key once', () => {
    const out = generateEnvTypes('FOO=1\nFOO=2\nBAR=3');
    expect((out.match(/FOO: string;/g) || []).length).toBe(1);
    expect((out.match(/BAR: string;/g) || []).length).toBe(1);
  });

  it('should skip lines where the key is not a valid identifier', () => {
    const out = generateEnvTypes('1BAD=fail\n_1GOOD=ok');
    expect(out).not.toContain('1BAD:');
    expect(out).toContain('_1GOOD: string;');
  });

  // Additional test: key with only numbers (should skip)
  it('should skip keys that start with a number', () => {
    const out = generateEnvTypes('123KEY=fail\nKEY123=ok');
    expect(out).not.toContain('123KEY:');
    expect(out).toContain('KEY123: string;');
  });

  // Additional branch test: ensure sanitizeKey coverage
  it('should not include keys with invalid characters', () => {
    const out = generateEnvTypes('MY-KEY=bad\nMY KEY=bad\nMY.KEY=bad');
    expect(out).not.toContain('MY-KEY:');
    expect(out).not.toContain('MY KEY:');
    expect(out).not.toContain('MY.KEY:');
  });
});