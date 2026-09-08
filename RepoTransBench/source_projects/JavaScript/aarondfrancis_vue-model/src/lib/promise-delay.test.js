// Correct import, export, and handling for promise-delay.js
const assert = require('assert');
const delay = require('./promise-delay');

describe('promise-delay', () => {
  it('delays for at least X ms', async () => {
    const start = Date.now();
    await delay(50);
    const elapsed = Date.now() - start;
    assert(elapsed >= 45, `Elapsed: ${elapsed}`);
  });
  it('returns resolved value', async () => {
    const v = await delay(10, 'foo');
    assert.strictEqual(v, 'foo');
  });
});