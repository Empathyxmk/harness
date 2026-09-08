let constants;
try {
  constants = require('../../parser/parser-constants.js');
} catch (e) {
  constants = {};
}

describe('Parser Constants (public)', () => {
  it('should export at least one constant property (public)', () => {
    expect(Object.keys(constants).length).toBeGreaterThan(0);
  });
  it('should export a VERSION field which is a non-empty string if present (public)', () => {
    if ('VERSION' in constants) {
      expect(typeof constants.VERSION).toBe('string');
      expect(constants.VERSION.length).toBeGreaterThan(0);
    }
  });
});