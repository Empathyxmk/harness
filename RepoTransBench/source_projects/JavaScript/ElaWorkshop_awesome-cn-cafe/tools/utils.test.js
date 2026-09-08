const utils = require('./utils');
const path = require('path');

describe('utils.js', () => {
  test('cities should be an array', () => {
    expect(Array.isArray(utils.cities)).toBe(true);
    expect(utils.cities.length).toBeGreaterThan(0);
  });

  test('getCityGeoJSON gives correct path', () => {
    const fileName = utils.getCityGeoJSON('beijing');
    expect(fileName.endsWith('beijing.geojson')).toBe(true);
  });

  test('ROOT_DIR and GEOJSON_EXT are correct', () => {
    expect(typeof utils.ROOT_DIR).toBe('string');
    expect(utils.GEOJSON_EXT).toBe('.geojson');
  });
});