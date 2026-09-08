import assert from 'node:assert/strict';
import config from '../index.js';

// Public: max-nesting-depth = 1, and ignoreAtRules must contain 'each', 'include'
assert.strictEqual(
  config.rules['max-nesting-depth'][0],
  1,
  'max-nesting-depth value should be 1'
);
assert.ok(
  config.rules['max-nesting-depth'][1].ignoreAtRules.includes('each'),
  'max-nesting-depth ignoreAtRules should include "each"'
);
assert.ok(
  config.rules['max-nesting-depth'][1].ignoreAtRules.includes('include'),
  'max-nesting-depth ignoreAtRules should include "include"'
);