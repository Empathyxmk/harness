// Test for index.js stylelint configuration

import assert from 'node:assert/strict';
import config from '../index.js';

function testBasicStructure() {
  assert.equal(typeof config, 'object', 'Export should be an object');
  assert.ok(Array.isArray(config.plugins), '"plugins" should be an array');
  assert.equal(config.customSyntax, 'postcss-scss', 'customSyntax must be postcss-scss');
  assert.ok('rules' in config, 'rules should exist');
  assert.equal(typeof config.rules, 'object', 'rules should be an object');
}

function testPluginValues() {
  assert(config.plugins.includes('stylelint-scss'), 'plugin stylelint-scss present');
  assert(config.plugins.includes('@stylistic/stylelint-plugin'), 'plugin stylistic present');
}

function testRuleTypesAndKeys() {
  // Check a sample of keys for presence and type
  assert.equal(config.rules['at-rule-disallowed-list'][0], 'debug');
  assert.equal(config.rules['color-hex-length'], 'short');
  assert.equal(config.rules['color-named'], 'never');
  assert.equal(config.rules['block-no-empty'], true);
  assert.equal(config.rules['at-rule-no-vendor-prefix'], true);
  assert.equal(config.rules['function-url-quotes'], 'always');
}

function testSassAndStylisticRules() {
  // Sass plugin rule
  assert.equal(config.rules['scss/at-extend-no-missing-placeholder'], true);
  // Stylistic plugin rule
  assert.equal(config.rules['@stylistic/block-opening-brace-space-before'], 'always');
}

function testComplexRuleValues() {
  // Rule with array value and options object
  assert(Array.isArray(config.rules['max-nesting-depth']), 'max-nesting-depth is array');
  // Rule with object value
  assert.equal(typeof config.rules['declaration-property-value-disallowed-list'], 'object');
  // Disallow-list object format check
  assert.ok(
    Object.keys(config.rules['declaration-property-value-disallowed-list']).length > 0,
    'declaration-property-value-disallowed-list has keys'
  );
}

function testNullConfigValue() {
  assert.equal(config.rules['at-rule-no-unknown'], null, 'Allow disabling a rule with null');
}

// Ensure that all rules use either true, false, string, array, or object as their value types
function testRuleValueTypes() {
  Object.entries(config.rules).forEach(([key, value]) => {
    const allowedTypes = ['boolean', 'string', 'object'];
    if (Array.isArray(value)) return;
    assert(
      allowedTypes.includes(typeof value),
      `Rule '${key}' must have allowed type, got ${typeof value}`
    );
  });
}

// Run all the defined tests
testBasicStructure();
testPluginValues();
testRuleTypesAndKeys();
testSassAndStylisticRules();
testComplexRuleValues();
testNullConfigValue();
testRuleValueTypes();