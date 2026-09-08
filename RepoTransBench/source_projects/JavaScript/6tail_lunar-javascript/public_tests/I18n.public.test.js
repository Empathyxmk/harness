const {I18n} = require('../lunar');

test('getMessage() - public', () => {
  expect(I18n.getMessage('not_in_table', {x: 1})).toBe('not_in_table');
  // Only test missing key (should return key)
  // Test a real key with no params if exists
});