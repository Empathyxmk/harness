// Public test for DataLoader abuse/corner cases using different input/output data.
// This file is intentionally using different data/setups than the original test.
// It must NOT duplicate the exact same values as src/__tests__/abuse.test.js.

const DataLoader = require('../src/index');

describe('DataLoader abuse/corner cases (public)', () => {
  it('Handles empty batch (public)', async () => {
    let callCount = 0;
    const loader = new DataLoader(async keys => {
      callCount++;
      return keys.map(k => k * 2);
    });

    // Using a scenario where loader.loadMany([]) should resolve to []
    const result = await loader.loadMany([]);
    expect(result).toEqual([]);
    // The batch function may or may not be called, but DataLoader spec says
    // for zero keys, batch function should NOT be called. So we expect 0
    expect(callCount).toBe(0);
  });

  it('Load with undefined key (public)', async () => {
    const loader = new DataLoader(async keys => keys);

    // This should throw a TypeError because undefined is not a valid key.
    await expect(() => loader.load(undefined)).toThrow(TypeError);
  });

  it('Allow loading falsy but valid values 0 and "" (public)', async () => {
    // This tests that falsy but valid keys (0, "") are allowed
    const loader = new DataLoader(async keys => keys.map(k => `out-${k}`));
    const result = await loader.loadMany([0, '']);
    expect(result).toEqual(['out-0', 'out-']);
  });
});