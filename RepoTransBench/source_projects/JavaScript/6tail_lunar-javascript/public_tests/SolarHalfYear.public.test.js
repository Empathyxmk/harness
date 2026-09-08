const { SolarHalfYear } = require('../lunar');

test('toString() - public', () => {
  const sh = SolarHalfYear.fromYm(2020, 1);
  expect(typeof sh.toString()).toBe('string');
  expect(sh.getMonths().length).toBe(6);
  expect(sh.getYear()).toBe(2020);
  expect(sh.getIndex()).toBe(1);
});