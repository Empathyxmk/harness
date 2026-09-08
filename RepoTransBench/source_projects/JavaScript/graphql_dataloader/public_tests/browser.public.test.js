/**
 * Test batching on browser environment - public with new data.
 */
const DataLoader = require('../src/index.js');

describe('DataLoader basic batching (browser variant, public)', () => {
  it('batches using different values (public)', async () => {
    const loader = new DataLoader(async keys => keys.map(k => k + 10));
    const result = await Promise.all([
      loader.load(100),
      loader.load(200),
      loader.load(300)
    ]);
    expect(result).toEqual([110, 210, 310]);
  });
});