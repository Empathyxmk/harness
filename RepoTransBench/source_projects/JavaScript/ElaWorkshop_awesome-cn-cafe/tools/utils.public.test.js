const utils = require('./utils');

describe('utils.js [PUBLIC]', () => {
  test('cities should be an array and contain at least one known city', () => {
    expect(Array.isArray(utils.cities)).toBe(true);
    expect(utils.cities.includes('beijing')).toBe(true); // different from >0, more specific
  });

  test('getCityGeoJSON gives correct path for wuhan', () => {
    const fileName = utils.getCityGeoJSON('wuhan');
    expect(fileName.endsWith('wuhan.geojson')).toBe(true);
  });

  test('ROOT_DIR and GEOJSON_EXT still correct', () => {
    expect(typeof utils.ROOT_DIR).toBe('string');
    expect(utils.GEOJSON_EXT.startsWith('.geo')).toBe(true); // now only .geojson makes this true
  });
});