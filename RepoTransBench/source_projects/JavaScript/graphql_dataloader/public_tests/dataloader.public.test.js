/**
 * Public test for general DataLoader batching with different data.
 */
const DataLoader = require('../src/index.js');

describe('DataLoader batch behavior (public test)', () => {
  it('returns squares of numbers, public data', async () => {
    const loader = new DataLoader(async keys => keys.map(x => x * x));
    const results = await loader.loadMany([3, 4, 5]);
    expect(results).toEqual([9, 16, 25]);
  });

  it('single load returns correct value, public data', async () => {
    const loader = new DataLoader(async keys => keys.map(x => x + 1));
    const result = await loader.load(10);
    expect(result).toBe(11);
  });
});