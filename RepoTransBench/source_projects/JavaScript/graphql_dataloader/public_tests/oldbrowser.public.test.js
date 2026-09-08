/**
 * Public tests for compatibility with old browsers (no setImmediate): different data.
 */
const DataLoader = require('../src/index.js');

describe('Old browser scenario (public)', () => {
  it('batches requests without setImmediate (public)', async () => {
    const calls = [];
    const loader = new DataLoader(async keys => {
      calls.push(keys);
      return keys;
    });
    // Make several loads synchronously, intentionally with new inputs
    const p1 = loader.load(21);
    const p2 = loader.load(22);
    const p3 = loader.load(23);
    const result = await Promise.all([p1, p2, p3]);
    expect(result).toEqual([21, 22, 23]);
    expect(calls.length).toBe(1); // All batched together
    expect(calls[0].sort()).toEqual([21, 22, 23]);
  });
});