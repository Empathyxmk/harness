/**
 * These tests simulate a browser-like environment for coverage of file protocol path.
 * We'll monkey-patch global.location/protocol for this file only.
 */

describe('stack-source-map: browser file protocol', () => {
  let stackSourceMap;
  let origLocation;

  beforeEach(() => {
    stackSourceMap = require('../index');
    origLocation = global.location;
    global.location = { protocol: 'file:' };
    // jest.restoreAllMocks not needed, just for clean-up
  });

  afterEach(() => {
    global.location = origLocation;
  });

  test('should not throw and warn when protocol is file:', () => {
    // Silence console.warn for test
    const warnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {});
    expect(() => stackSourceMap()).not.toThrow();
    expect(warnSpy).toHaveBeenCalledWith(expect.stringContaining('not works on file protocol'));
    warnSpy.mockRestore();
  });
});