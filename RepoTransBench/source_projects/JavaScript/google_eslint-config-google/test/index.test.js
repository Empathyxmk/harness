// Purpose: Directly test index.js exports and rule structure

const conf = require('../index.js');

describe('eslint-config-google exports', () => {
  test('should export an object', () => {
    expect(typeof conf).toBe('object');
    expect(conf).toHaveProperty('rules');
    expect(typeof conf.rules).toBe('object');
  });

  test('should include specific rules', () => {
    // Test for some explicit rules
    expect(conf.rules).toHaveProperty('no-cond-assign', 'off');
    expect(conf.rules).toHaveProperty('no-irregular-whitespace', 'error');
    expect(conf.rules).toHaveProperty('no-unexpected-multiline', 'error');
    expect(conf.rules).toHaveProperty('curly');
    expect(Array.isArray(conf.rules.curly)).toBe(true);
    expect(conf.rules.curly[0]).toBe('error');
    expect(conf.rules.curly[1]).toBe('multi-line');
  });

  test('should not override commented-out rules', () => {
    // A commented out rule should not be present (as a string rule only).
    expect(conf.rules).not.toHaveProperty('no-console');
    expect(conf.rules).not.toHaveProperty('no-empty-character-class');
  });

  test('should not crash when listing all rule keys', () => {
    expect(Object.keys(conf.rules).length).toBeGreaterThan(0);
  });
});