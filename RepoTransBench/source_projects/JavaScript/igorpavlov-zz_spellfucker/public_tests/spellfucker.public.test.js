const spellfucker = require('../src/spellfucker');

describe('spellfucker (public tests, different data)', () => {
  it('should mutate simple word (world)', () => {
    const result = spellfucker('world');
    expect(result).not.toBe('world');
    expect(typeof result).toBe('string');
  });

  it('should work with multi-line strings (different lines)', () => {
    const str = 'foo\nbar';
    const res = spellfucker(str);
    expect(res.split('\n').length).toBe(2);
  });

  it('should work with whitespace-only string', () => {
    expect(spellfucker(' \t\n')).toBe(' \t\n');
  });

  it('should not throw on null or undefined (again)', () => {
    expect(() => spellfucker(null)).not.toThrow();
    expect(() => spellfucker(undefined)).not.toThrow();
    expect(spellfucker(null)).toBe('');
    expect(spellfucker(undefined)).toBe('');
  });

  it('should not mutate math operators (!@#$%)', () => {
    expect(spellfucker('!@#$%')).toBe('!@#$%');
  });

  it('should not overly shrink longer words', () => {
    let orig = 'mississippi';
    expect(spellfucker(orig).length).toBeGreaterThan(0);
    expect(Math.abs(spellfucker(orig).length - orig.length)).toBeLessThan(orig.length);
  });

  it('should mutate sentence with different words', () => {
    let s = 'Another different example phrase.';
    let m = spellfucker(s);
    expect(m.length).toBeGreaterThan(0);
    expect(m).not.toBe(s);
  });

  it('should not error on other gibberish', () => {
    let res = spellfucker('qwer!!__==00xx??');
    expect(typeof res).toBe('string');
  });

  it('should not error on a single tab', () => {
    expect(spellfucker('\t')).toBe('\t');
  });
});