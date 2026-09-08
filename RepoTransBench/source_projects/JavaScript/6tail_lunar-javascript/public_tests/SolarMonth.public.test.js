const {SolarMonth} = require('../lunar');

test('toString() - public', () => {
  const m = SolarMonth.fromYm(1990, 8);
  expect(typeof m.toString()).toBe('string');
  expect(m.getYear()).toBe(1990);
  expect(m.getMonth()).toBe(8);
  expect(m.getDays().length).toBeGreaterThanOrEqual(28);
});