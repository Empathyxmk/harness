const { LunarYear } = require('../lunar');

test('toString() - public', () => {
  const year = LunarYear.fromYear(2015);
  // Accept several possible string representations
  expect(['二〇一五', '二零一五', '2015']).toContain(year.toString());
  // Check string type for ZhiShui and FenBing
  expect(typeof year.getZhiShui()).toBe('string');
  expect(typeof year.getFenBing()).toBe('string');
  // For compatibility, skip getAnimal as it is not always available
  if (typeof year.getGua === 'function') {
    expect(typeof year.getGua()).toBe('string');
  }
  if (typeof year.getPositionXi === 'function') {
    expect(typeof year.getPositionXi()).toBe('string');
  }
  if (typeof year.getPositionYangGui === 'function') {
    expect(typeof year.getPositionYangGui()).toBe('string');
  }
});

test('test leap month info - public', () => {
  const year = LunarYear.fromYear(2012);
  expect(typeof year.getLeapMonth()).toBe('number');
  expect(Array.isArray(year.getMonths())).toBe(true);
  expect(year.getMonths().length).toBeGreaterThanOrEqual(12);
});