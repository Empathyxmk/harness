const assert = require('assert');

describe('Root index.js', () => {
  it('should export the same as require("./lib")', () => {
    const exported = require('../../index.js');
    const libManual = require('../../lib');
    assert.strictEqual(exported, libManual);
  });
});