import assert from 'node:assert/strict';
import config from '../index.js';

// Public: block-no-empty should be true, and color-no-invalid-hex should be true (2 rules together)
assert.equal(config.rules['block-no-empty'], true, 'block-no-empty should be true');
assert.equal(config.rules['color-no-invalid-hex'], true, 'color-no-invalid-hex should be true (public batch test)');