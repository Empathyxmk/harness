const {Lunar} = require('../lunar');

test('getStartYear() - public', () => {
  const lunar = Lunar.fromYmdHms(1993, 3, 6, 8, 50, 0);
  if (typeof lunar.getYun === 'function') {
    const yun = lunar.getYun(1, 0);
    expect(yun.getStartYear()).toBeGreaterThan(1993);
  }
});

test('getStartSolar() - public', () => {
  const lunar = Lunar.fromYmdHms(1993, 3, 6, 8, 50, 0);
  if (typeof lunar.getYun === 'function') {
    const yun = lunar.getYun(1, 0);
    expect(yun.getStartSolar().getYear()).toBeGreaterThan(1993 - 1);
  }
});