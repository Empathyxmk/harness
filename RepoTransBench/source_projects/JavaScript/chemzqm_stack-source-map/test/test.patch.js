const stackSourceMap = require('../index');

describe('stack-source-map: Patch scenarios', () => {
  test('should handle repeated calls', () => {
    // Should not throw if called multiple times
    stackSourceMap();
    stackSourceMap();
    stackSourceMap({});
  });

  test('should not throw if called with bogus options', () => {
    stackSourceMap({ foo: 123, bar: false });
  });

  test('should allow override of options', () => {
    const prepareStackTrace = jest.fn();
    stackSourceMap({ prepareStackTrace });
    stackSourceMap();
  });
});