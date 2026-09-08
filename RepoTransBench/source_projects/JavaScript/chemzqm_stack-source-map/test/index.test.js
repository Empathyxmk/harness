// These tests target Node.js env *only*, where location is not defined
describe('stack-source-map: Node.js environment', () => {
  let stackSourceMap, restore;
  beforeEach(() => {
    jest.resetModules();
    // Remove or backup global.location to ensure correct Node simulation
    restore = global.location;
    delete global.location;
    stackSourceMap = require('../index');
  });

  afterEach(() => {
    // Restore location if it existed
    if (restore !== undefined) global.location = restore;
    else delete global.location;
  });

  test('exports a function', () => {
    expect(typeof stackSourceMap).toBe('function');
  });

  // All code paths: 'location' is not defined, so if-access throws in unguarded code
  test('invoking stackSourceMap does not throw when "location" is not defined', () => {
    // Patch index.js: temporarily override the references so no unguarded location
    // But actually, original code will always ReferenceError!
    // So, instead, we wrap location access with typeof in index.js to fix tests.
    // --- This test will always fail unless index.js is patched to guard "location" access ---
    expect(() => stackSourceMap()).not.toThrow();
  });

  test('invoking stackSourceMap with options does not throw', () => {
    expect(() =>
      stackSourceMap({
        prepareStackTrace: jest.fn(),
        ErrorStackParser: { parse: jest.fn() }
      })
    ).not.toThrow();
  });

  test('sets Error.prepareStackTrace in Node env if no prepareStackTrace passed', () => {
    stackSourceMap();
    expect(typeof Error.prepareStackTrace).toBe('function');
  });

  test('uses provided prepareStackTrace from options', () => {
    const mock = jest.fn();
    stackSourceMap({ prepareStackTrace: mock });
    expect(Error.prepareStackTrace).toBe(mock);
  });

  test('does not throw if ErrorStackParser is provided', () => {
    const parseMock = jest.fn();
    stackSourceMap({ ErrorStackParser: { parse: parseMock } });
    expect(Error.prepareStackTrace).toBeDefined();
  });
});