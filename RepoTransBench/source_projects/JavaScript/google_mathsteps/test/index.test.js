const index = require('../index');

describe('index.js exports', () => {
  it('should properly export factor', () => {
    expect(index.factor).toBeDefined();
    // It is a function, not object!
    expect(typeof index.factor).toBe('function');
  });

  it('should properly export simplifyExpression', () => {
    expect(index.simplifyExpression).toBeDefined();
    // It is a function, not object!
    expect(typeof index.simplifyExpression).toBe('function');
    // If it's a function, should be callable
    expect(() => index.simplifyExpression('x+1')).not.toThrow();
  });

  it('should properly export solveEquation', () => {
    expect(index.solveEquation).toBeDefined();
    // It is a function, not object!
    expect(typeof index.solveEquation).toBe('function');
    // Should not throw here, test with dummy arguments
    expect(() => index.solveEquation('x=1')).not.toThrow();
  });
});