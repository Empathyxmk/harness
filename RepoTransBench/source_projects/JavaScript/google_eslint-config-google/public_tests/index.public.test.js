// Purpose: Public tests for index.js exports and rule structure (different test data)

const conf = require('../index.js');

describe('eslint-config-google exports - PUBLIC', () => {
  test('should export a non-null object', () => {
    expect(conf && typeof conf).toBe('object');
    expect(Object.prototype.hasOwnProperty.call(conf, 'rules')).toBe(true);
    expect(typeof conf.rules).toBe('object');
  });

  test('should include a different set of specific rules', () => {
    // Pick rules that actually exist in this config for public test, but not the same as existing test
    // 'quotes' is present and is an array, contains 'error'
    expect(conf.rules).toHaveProperty('quotes');
    expect(Array.isArray(conf.rules.quotes)).toBe(true);
    expect(conf.rules.quotes[0]).toBe('error');

    // Use 'indent', which is also present and is an array
    expect(conf.rules).toHaveProperty('indent');
    expect(Array.isArray(conf.rules.indent)).toBe(true);
    expect(conf.rules.indent[0]).toBe('error');
    expect(typeof conf.rules.indent[1]).toBe('number');

    // Pick a rule that is set to 'off' in this config ('array-bracket-newline')
    expect(conf.rules).toHaveProperty('array-bracket-newline', 'off');
  });

  test('should still omit other commented-out rules', () => {
    // Use obviously omitted rules
    expect(conf.rules).not.toHaveProperty('no-alert');
    expect(conf.rules).not.toHaveProperty('no-script-url');
  });

  test('should have a decent number of rule keys (threshold public)', () => {
    expect(Object.keys(conf.rules).length).toBeGreaterThan(10);
  });
});