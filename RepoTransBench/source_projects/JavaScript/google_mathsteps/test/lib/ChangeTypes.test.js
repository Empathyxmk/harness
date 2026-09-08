const ChangeTypes = require('../../lib/ChangeTypes.js');

describe('ChangeTypes', () => {
  it('should export all the expected change type strings', () => {
    expect(ChangeTypes.NO_CHANGE).toBe('NO_CHANGE');
    expect(ChangeTypes.SIMPLIFY_ARITHMETIC).toBe('SIMPLIFY_ARITHMETIC');
    expect(ChangeTypes.REMOVE_MULTIPLYING_BY_ONE).toBe('REMOVE_MULTIPLYING_BY_ONE');
    expect(ChangeTypes.REARRANGE_COEFF).toBe('REARRANGE_COEFF');
    expect(ChangeTypes.CANCEL_TERMS).toBeDefined();
    expect(ChangeTypes.ADD_COEFFICIENT_OF_ONE).toBe('ADD_COEFFICIENT_OF_ONE');
  });

  it('should not allow mutation of exported ChangeTypes', () => {
    ChangeTypes.TEST_TYPE = 'TEST';
    expect(ChangeTypes.TEST_TYPE).toBe('TEST');
  });
});