// Sanity test for parser-constants.js

const constants = require('./parser-constants');

describe('parser-constants module', () => {
  it('should export an object or constants', () => {
    expect(typeof constants).toBe('object');
    expect(Object.keys(constants).length).toBeGreaterThan(0);
  });
});