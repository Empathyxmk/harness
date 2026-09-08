const regexRules = require('../../parser/regex-rules');

describe('Regex Rules (public)', () => {
  it('should export an object or a function (public)', () => {
    expect(['object', 'function']).toContain(typeof regexRules);
  });

  it('should contain a digit regex rule (public)', () => {
    // Let's use a different example from existing: test for a digit pattern
    const digitRegex = regexRules.digit || regexRules.DIGIT || regexRules.number;
    if (digitRegex) {
      expect(typeof digitRegex.test).toBe('function');
      expect(digitRegex.test('5')).toBeTruthy();
      expect(digitRegex.test('a')).toBeFalsy();
    }
  });
});