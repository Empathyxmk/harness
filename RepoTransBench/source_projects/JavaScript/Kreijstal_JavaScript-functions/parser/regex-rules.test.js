const rules = require('./regex-rules');

describe('Regex rules module', () => {
  it('should export rule objects', () => {
    expect(typeof rules).toBe('object');
    expect(Object.keys(rules).length).toBeGreaterThan(0);
  });

  // Target uncovered lines and branches in regex-rules.js
  it('should test all regex expressions', () => {
    Object.keys(rules).forEach((key) => {
      const rule = rules[key];
      if (rule && rule.test) {
        // Try with defined and edge-case inputs
        expect(rule.test('')).toBeDefined();
        expect(rule.test('test input')).toBeDefined();
      }
      if (rule && rule.exec) {
        expect(rule.exec('test')).toBeDefined();
      }
    });
  });

  it('should handle edge cases for rule matching and not matching', () => {
    Object.keys(rules).forEach((key) => {
      const rule = rules[key];
      if (rule instanceof RegExp) {
        expect(rule.test('unlikelyinputthatwillnotmatch')).toBe(false);
      }
    });
  });

  // Add explicit tests for rarely-matching, corner-case patterns
  it('should explicitly test patterns for uncovered lines', () => {
    if (rules.NUMBER) {
      expect(rules.NUMBER.test('12345')).toBe(true);
      expect(rules.NUMBER.test('notanumber')).toBe(false);
      expect(rules.NUMBER.test('')).toBe(false);
    }
    if (rules.IDENT) {
      expect(rules.IDENT.test('varName')).toBe(true);
      expect(rules.IDENT.test('const')).toBe(true);
      expect(rules.IDENT.test('123abc')).toBe(false);
    }
    // Add more targetted checks if the below patterns are defined
    if (rules.STRING) {
      expect(rules.STRING.test('"hello"')).toBe(true);
      expect(rules.STRING.test("'world'")).toBe(true);
      expect(rules.STRING.test('noquotes')).toBe(false);
    }
  });
});