import assert from 'node:assert/strict';
import config from '../index.js';

// Public: function-url-quotes should be always and color-hex-length short (batch public check)
assert.strictEqual(
  config.rules['function-url-quotes'],
  'always',
  'function-url-quotes should be always'
);
assert.strictEqual(
  config.rules['color-hex-length'],
  'short',
  'color-hex-length should be short'
);