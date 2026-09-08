// Public: These tests target Node.js env only, using different test data variations

describe('stack-source-map: Node.js environment - public tests', () => {
  let stackSourceMap, restore;
  beforeEach(() => {
    jest.resetModules();
    restore = global.location;
    delete global.location;
    stackSourceMap = require('../index');
  });

  afterEach(() => {
    if (restore !== undefined) global.location = restore;
    else delete global.location;
  });

  test('exports a callable entity (function)', () => {
    // Altered description/text for public test case
    expect(typeof stackSourceMap).toBe('function');
  });

  test('invoking stackSourceMap does not throw with no arguments', () => {
    // Changed call approach by passing undefined value explicitly
    expect(() => stackSourceMap(undefined)).not.toThrow();
  });

  test('invoking stackSourceMap with different options object does not throw', () => {
    // Pass in different mock implementations for public variant
    expect(() =>
      stackSourceMap({
        prepareStackTrace: () => {},
        ErrorStackParser: { parse: () => ({}) }
      })
    ).not.toThrow();
  });

  test('sets Error.prepareStackTrace when called with no prepareStackTrace option', () => {
    // Confirm property type via strict equality to "function" (no change in expectation)
    stackSourceMap();
    expect(typeof Error.prepareStackTrace).toBe('function');
  });

  test('uses user-provided prepareStackTrace from options (different mock)', () => {
    const mockPrepare = function custom() {};
    stackSourceMap({ prepareStackTrace: mockPrepare });
    expect(Error.prepareStackTrace).toBe(mockPrepare);
  });

  test('does not throw if ErrorStackParser is a custom object', () => {
    const mockParse = () => 'parsed';
    stackSourceMap({ ErrorStackParser: { parse: mockParse } });
    expect(typeof Error.prepareStackTrace).toBe('function');
  });
});