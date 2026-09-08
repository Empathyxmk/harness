const {SolarUtil} = require('../lunar');

test('isLeapYear() - public', () => {
  expect(SolarUtil.isLeapYear(1976)).toBe(true);
  expect(SolarUtil.isLeapYear(1999)).toBe(false);
  expect(SolarUtil.isLeapYear(2400)).toBe(true);
  expect(SolarUtil.isLeapYear(2100)).toBe(false);
});

test('getDaysInYear() - public', () => {
  expect(SolarUtil.getDaysOfYear(2016)).toBe(366); // leap year
  expect(SolarUtil.getDaysOfYear(2019)).toBe(365); // non leap year
});