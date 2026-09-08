import assert from 'node:assert/strict';
import config from '../index.js';

// Public: Check for a different value on 'at-rule-disallowed-list'
assert.ok(
  Array.isArray(config.rules['at-rule-disallowed-list']),
  'at-rule-disallowed-list should be an array');
assert.ok(
  config.rules['at-rule-disallowed-list'].includes('debug'),
  'at-rule-disallowed-list should contain "debug"'
);
// Test that a different known-at-rule is NOT blocked (test data difference)
assert.ok(
  !config.rules['at-rule-disallowed-list'].includes('warn'),
  'at-rule-disallowed-list must not contain "warn" (public test)'
);