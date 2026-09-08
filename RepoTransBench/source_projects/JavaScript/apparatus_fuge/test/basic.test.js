// Patch: fix incorrect path, should be './helpers/runner' not '../helpers/runner'
const assert = require('assert');
const fugeMod = require('./helpers/runner');

describe('fuge basic', () => {
  it('should export a function', () => {
    assert.strictEqual(typeof fugeMod, 'function');
  });
  it('should return a runner object if given config', () => {
    const runner = fugeMod({});
    assert.ok(runner);
    assert.strictEqual(typeof runner, 'object');
  });
});