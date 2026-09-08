const fs = require('fs');
const path = require('path');
const lint = require('./lint');
const utils = require('./utils');

const tempCity = 'publiccity';
const cityGeoPath = utils.getCityGeoJSON(tempCity);

beforeAll(() => {
  utils.cities.splice(0, utils.cities.length, tempCity);

  // Public geojson and README with different values (营业 and 整修)
  fs.writeFileSync(cityGeoPath, JSON.stringify({
    type: 'FeatureCollection',
    features: [
      { properties: { "营业状态": "营业" } },
      { properties: { "营业状态": "整修" } }
    ]
  }, null, 2));
  fs.writeFileSync(path.resolve(__dirname, '../README.md'), `
    | City      | 咖啡馆数量 |
    |-----------|-----------|
    | publiccity | 3 |
  `);
});

afterAll(() => {
  try { fs.unlinkSync(cityGeoPath); } catch {}
  try { fs.unlinkSync(path.resolve(__dirname, '../README.md')); } catch {}
});

describe('lint.js [PUBLIC]', () => {
  test('checkGeoJSON works for city', () => {
    global.console = { log: jest.fn(), warn: jest.fn(), error: jest.fn() };
    expect(lint.checkGeoJSON()).toBe(undefined);
    expect(console.log).toHaveBeenCalled();
  });

  test('checkGeoJSON returns false on missing file', () => {
    fs.unlinkSync(cityGeoPath);
    global.console = { log: jest.fn(), warn: jest.fn(), error: jest.fn() };
    expect(lint.checkGeoJSON()).toBe(undefined);
    expect(console.warn).toHaveBeenCalled();
    // Restore for following tests
    fs.writeFileSync(cityGeoPath, JSON.stringify({
      type: 'FeatureCollection', features: []
    }, null, 2));
  });

  test('updateCafeNumbers updates README cafenumbers', () => {
    // set README number for publiccity to 6 to guarantee change
    fs.writeFileSync(path.resolve(__dirname, '../README.md'), `
      | City      | 咖啡馆数量 |
      |-----------|-----------|
      | publiccity | 6 |
    `);
    fs.writeFileSync(cityGeoPath, JSON.stringify({
      type: "FeatureCollection",
      features: [{} , {}, {}, {}]
    }, null, 2));
    global.console = { log: jest.fn(), warn: jest.fn(), error: jest.fn() };
    lint.updateCafeNumbers();
    const readme = fs.readFileSync(path.resolve(__dirname, '../README.md'), 'utf-8');
    expect(readme).toMatch(/\| publiccity \| 4 \|/);
    expect(console.log).toHaveBeenCalled();
  });

  test('checkNumbers catches inconsistency', () => {
    fs.writeFileSync(path.resolve(__dirname, '../README.md'), `
      | City      | 咖啡馆数量 |
      |-----------|-----------|
      | publiccity | 9 |
    `);
    fs.writeFileSync(cityGeoPath, JSON.stringify({
      type: "FeatureCollection",
      features: [{}, {}, {}]
    }, null, 2));
    global.console = { log: jest.fn(), warn: jest.fn(), error: jest.fn() };
    lint.checkNumbers();
    expect(console.log).toHaveBeenCalled();
  });

  test('checkGeoJSON handles empty features gracefully', () => {
    fs.writeFileSync(cityGeoPath, JSON.stringify({ type: "FeatureCollection", features: [] }, null, 2));
    global.console = { log: jest.fn(), warn: jest.fn(), error: jest.fn() };
    lint.checkGeoJSON();
    expect(true).toBeTruthy();
  });

  test('checkGeoJSON handles missing properties gracefully', () => {
    fs.writeFileSync(cityGeoPath, JSON.stringify({
      type: "FeatureCollection",
      features: [{}, { properties: undefined }]
    }, null, 2));
    global.console = { log: jest.fn(), warn: jest.fn(), error: jest.fn() };
    lint.checkGeoJSON();
    expect(console.warn).toHaveBeenCalled();
  });

  test('getCafeNumbersFromReadme extracts correct numbers', () => {
    fs.writeFileSync(path.resolve(__dirname, '../README.md'), `
      | City      | 咖啡馆数量 |
      |-----------|-----------|
      | publiccity | 11 |
    `);
    const numbers = lint.getCafeNumbersFromReadme();
    expect(numbers['publiccity']).toBe(11);
  });

  test('getCafeNumberFromGeo returns correct feature count', () => {
    fs.writeFileSync(cityGeoPath, JSON.stringify({
      type: "FeatureCollection",
      features: [{ properties: {} }, { properties: {} }]
    }, null, 2));
    expect(lint.getCafeNumberFromGeo(tempCity)).toBe(2);
  });

  test('isCounterMatched detects match', () => {
    fs.writeFileSync(cityGeoPath, JSON.stringify({
      type: "FeatureCollection",
      features: [{}, {}, {}, {}, {}]
    }, null, 2));
    fs.writeFileSync(path.resolve(__dirname, '../README.md'), `
      | City      | 咖啡馆数量 |
      |-----------|-----------|
      | publiccity | 5 |
    `);
    expect(lint.isCounterMatched(tempCity, 5)).toBe(true);
    expect(lint.isCounterMatched(tempCity, 6)).toBe(false);
  });

  test('getCafeNumberFromGeo returns 0 for missing file', () => {
    try { fs.unlinkSync(cityGeoPath); } catch {}
    expect(lint.getCafeNumberFromGeo(tempCity)).toBe(0);
    fs.writeFileSync(cityGeoPath, JSON.stringify({ type: "FeatureCollection", features: [] }, null, 2));
  });

  test('getCafeNumberFromGeo returns 0 for malformed geojson', () => {
    fs.writeFileSync(cityGeoPath, '{ not real json');
    expect(() => lint.getCafeNumberFromGeo(tempCity)).toThrow();
    fs.writeFileSync(cityGeoPath, JSON.stringify({ type: "FeatureCollection", features: [] }, null, 2));
  });
});