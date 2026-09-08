// Extended test: ensure the module export is testable and covers conditional logic if any

const dangleModule = require('./dangle.module.js');

describe('dangle module', () => {
  it('should be a function', () => {
    expect(typeof dangleModule).toBe('function');
  });

  it('should return "dangle" when called', () => {
    expect(dangleModule()).toBe('dangle');
  });
});