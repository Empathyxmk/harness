const {SolarYear} = require('../lunar');

test('toString() - public', () => {
  const y = SolarYear.fromYear(2024);
  expect(typeof y.toString()).toBe('string');
  expect(y.getYear()).toBe(2024);
  expect(y.getMonths().length).toBe(12);
});