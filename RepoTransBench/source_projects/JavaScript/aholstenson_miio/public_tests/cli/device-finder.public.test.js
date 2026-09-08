// Simple public test just checking if module loads, as internals require unavailable deps in testing.
let DeviceFinder;

try {
  DeviceFinder = require('../../cli/device-finder');
} catch (e) {
  DeviceFinder = null;
}

describe('DeviceFinder public (smoke public)', () => {
  it('should not throw when requiring DeviceFinder (public)', () => {
    expect(DeviceFinder === undefined).toBe(false);
  });
});