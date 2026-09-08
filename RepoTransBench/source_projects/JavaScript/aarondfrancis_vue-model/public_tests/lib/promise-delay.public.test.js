const assert = require('assert');
const delay = require('../../src/lib/promise-delay');

describe('delay (public)', () => {
  it('delays for a different ms and resolves', async function() {
    const before = Date.now();
    await delay(30);
    const after = Date.now();
    assert.ok(after - before >= 28); // a little leeway
  });

  it('delays 0 ms and resolves immediately', async function() {
    const before = Date.now();
    await delay(0);
    const after = Date.now();
    assert.ok(after - before >= 0);
  });
});