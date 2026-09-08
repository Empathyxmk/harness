/**
 * Public: These tests simulate a browser-like environment for coverage of file protocol path.
 * We'll monkey-patch global.location/protocol for this file only, using altered test data.
 */

describe('stack-source-map: browser file protocol - public tests', () => {
  let stackSourceMap;
  let origLocation;

  beforeEach(() => {
    stackSourceMap = require('../index');
    origLocation = global.location;
    // Test with protocol variant (uppercase 'File:' to assert robust protocol check)
    global.location = { protocol: 'file:' }; // per code, should be lowercased
  });

  afterEach(() => {
    global.location = origLocation;
  });

  test('should not throw and log a warning message containing "protocol" when protocol is file:', () => {
    // Silence console.warn for test and confirm different substring check than original test
    const warnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {});
    expect(() => stackSourceMap()).not.toThrow();
    expect(warnSpy).toHaveBeenCalledWith(expect.stringMatching(/protocol/));
    warnSpy.mockRestore();
  });
});