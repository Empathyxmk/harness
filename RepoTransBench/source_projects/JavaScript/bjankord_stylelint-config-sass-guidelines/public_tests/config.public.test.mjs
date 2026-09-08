// Public test for index.js configuration - using different key checks than standard sanity/private checks
import assert from 'node:assert/strict';
import config from '../index.js';

assert.ok(Array.isArray(config.plugins), 'plugins should be an array');
assert.ok(config.plugins.includes('@stylistic/stylelint-plugin'), 'Should include @stylistic/stylelint-plugin plugin');
assert.equal(config.customSyntax, 'postcss-scss', 'customSyntax should be postcss-scss');
// Use a rule not usually checked as first/sanity: color-named
assert.equal(config.rules['color-named'], 'never', 'color-named rule should be never');
// Check that a stylistic/ rule exists and is set
assert.equal(config.rules['@stylistic/declaration-colon-space-after'], 'always-single-line', 'declaration-colon-space-after should be always-single-line');
// Check a scss/ rule present: scss/at-function-pattern
assert.ok(config.rules['scss/at-function-pattern'], 'scss/at-function-pattern should be set');

// Add a check for an ignoreAtRules value that is not commonly a first choice
assert.ok(
  Array.isArray(config.rules['max-nesting-depth'][1]?.ignoreAtRules),
  'max-nesting-depth option should have ignoreAtRules as array'
);
assert.ok(
  config.rules['max-nesting-depth'][1].ignoreAtRules.includes('supports'),
  'ignoreAtRules should include supports'
);

// Check that there is no rule called "nonexistent-fake-rule" to prove negative scenario
assert.equal(config.rules['nonexistent-fake-rule'], undefined, 'There must not be a rule "nonexistent-fake-rule"');