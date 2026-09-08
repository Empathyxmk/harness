const assert = require('assert');

describe('Root index.js (public)', () => {
  it('should export the same as requiring lib/index.js explicitly', () => {
    const main = require('../../index.js');
    const libExplicit = require('../../lib/index.js');
    assert.strictEqual(main, libExplicit);
  });
});