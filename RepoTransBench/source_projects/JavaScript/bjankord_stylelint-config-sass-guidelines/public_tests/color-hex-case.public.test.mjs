import assert from 'node:assert/strict';
import config from '../index.js';

// Public: color-hex-case should be lower, block-opening-brace-space-before always
assert.strictEqual(
  config.rules['@stylistic/color-hex-case'],
  'lower',
  '@stylistic/color-hex-case should be lower'
);
assert.strictEqual(
  config.rules['@stylistic/block-opening-brace-space-before'],
  'always',
  '@stylistic/block-opening-brace-space-before should be always'
);