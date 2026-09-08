import assert from 'node:assert/strict';
import config from '../index.js';

// Public: property-no-unknown and property-no-vendor-prefix should both be true
assert.strictEqual(
  config.rules['property-no-unknown'],
  true,
  'property-no-unknown should be true (public)'
);
assert.strictEqual(
  config.rules['property-no-vendor-prefix'],
  true,
  'property-no-vendor-prefix should be true (public)'
);