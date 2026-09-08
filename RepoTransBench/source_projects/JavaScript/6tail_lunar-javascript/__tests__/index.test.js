const index = require('../index.js');
const lunar = require('../lunar.js');

describe('index.js exports', () => {
  const expectedKeys = [
    'Solar', 'Lunar', 'Foto', 'Tao', 'NineStar', 'EightChar', 'SolarWeek', 'SolarMonth',
    'SolarSeason', 'SolarHalfYear', 'SolarYear', 'LunarMonth', 'LunarYear', 'LunarTime',
    'ShouXingUtil', 'SolarUtil', 'LunarUtil', 'FotoUtil', 'TaoUtil', 'HolidayUtil',
    'NineStarUtil', 'I18n'
  ];

  test('should export all the expected properties', () => {
    expectedKeys.forEach(k => {
      expect(index).toHaveProperty(k);
    });
  });

  test('exported objects should be the same as lunar.js exports', () => {
    expectedKeys.forEach(k => {
      expect(index[k]).toBe(lunar[k]);
    });
  });
});