// PATCH: Null/undefined/empty now returns '' for null/undefined
const spellfucker = require('../src/spellfucker');

describe('spellfucker', () => {
  it('should mutate simple word (hello)', () => {
    const result = spellfucker('hello');
    expect(result).not.toBe('hello');
    expect(typeof result).toBe('string');
  });

  it('should work with multi-line strings', () => {
    const str = 'hello\nworld';
    const res = spellfucker(str);
    expect(res.split('\n').length).toBe(2);
  });

  it('should work with empty string', () => {
    expect(spellfucker('')).toBe('');
  });

  it('should not throw on null or undefined', () => {
    expect(() => spellfucker(null)).not.toThrow();
    expect(() => spellfucker(undefined)).not.toThrow();
    expect(spellfucker(null)).toBe('');
    expect(spellfucker(undefined)).toBe('');
  });

  it('should not mutate punctuation', () => {
    expect(spellfucker('..,!?')).toBe('..,!?');
  });

  it('should not overly shrink words', () => {
    let orig = 'bananana';
    expect(spellfucker(orig).length).toBeGreaterThan(0);
    expect(Math.abs(spellfucker(orig).length - orig.length)).toBeLessThan(orig.length);
  });

  it('should mutate multiple words in a sentence', () => {
    let s = 'This is an example sentence.';
    let m = spellfucker(s);
    expect(m.length).toBeGreaterThan(0);
    expect(m).not.toBe(s);
  });

  it('should not error on gibberish input', () => {
    let res = spellfucker('asdklj2398u4__--==++');
    expect(typeof res).toBe('string');
  });

  it('should not error on whitespace-only', () => {
    expect(spellfucker('    \n \t')).toBe('    \n \t');
  });
});