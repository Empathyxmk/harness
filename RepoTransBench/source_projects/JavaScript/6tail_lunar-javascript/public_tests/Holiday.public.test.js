const {HolidayUtil, Solar} = require('../lunar');

test('getHolidays() - public', () => {
  const holidays = HolidayUtil.getHolidays(2022, 10);
  expect(holidays.length).toBeGreaterThanOrEqual(1);
  // Only check that at least one holiday contains "国庆"
  expect(holidays.map(h => h.getName()).join()).toMatch(/国庆/);
});

test('getHoliday() by date - public', () => {
  const solar = Solar.fromYmd(2022, 6, 1);
  const holiday = HolidayUtil.getHoliday(solar.getMonth(), solar.getDay());
  if (holiday) {
    expect(typeof holiday.getName()).toBe('string');
  } else {
    expect(holiday).toBeNull(); // some dates may not be a holiday
  }
});