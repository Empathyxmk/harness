const dangleModule = require('../src/dangle.module.js');

describe('dangle module (public)', () => {
  it('should still be a function type', () => {
    expect(typeof dangleModule).toBe('function');
  });

  it('should return "dangle" when invoked in a public test', () => {
    // This primarily can only return "dangle", so no alternative input.
    expect(dangleModule()).toBe('dangle');
  });
});