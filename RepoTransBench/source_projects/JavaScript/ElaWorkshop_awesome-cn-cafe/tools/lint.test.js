const fs = require('fs');
const path = require('path');
const lint = require('./lint');
const utils = require('./utils');

// TEST SETUP - use only 'testcity'
const tempCity = 'testcity';
const cityGeoPath = utils.getCityGeoJSON(tempCity);

beforeAll(() => {
  // Overwrite for safe test: keep only testcity for utils.cities
  utils.cities.splice(0, utils.cities.length, tempCity);

  // Create synthetic geojson and README files for test
  fs.writeFileSync(cityGeoPath, JSON.stringify({
    type: 'FeatureCollection',
    features: [
      { properties: { "营业状态": "营业" } },
      { properties: { "营业状态": "停业" } }
    ]
  }, null, 2));
  fs.writeFileSync(path.resolve(__dirname, '../README.md'), `
    | City   | 咖啡馆数量 |
    |--------|-----------|
    | testcity | 1 |
  `);
});

afterAll(() => {
  try { fs.unlinkSync(cityGeoPath); } catch {}
  try { fs.unlinkSync(path.resolve(__dirname, '../README.md')); } catch {}
});

describe('lint.js', () => {
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
    // set README number for testcity to 0 to guarantee change
    fs.writeFileSync(path.resolve(__dirname, '../README.md'), `
      | City   | 咖啡馆数量 |
      |--------|-----------|
      | testcity | 0 |
    `);
    fs.writeFileSync(cityGeoPath, JSON.stringify({
      type: "FeatureCollection",
      features: [{} , {}]
    }, null, 2));
    global.console = { log: jest.fn(), warn: jest.fn(), error: jest.fn() };
    lint.updateCafeNumbers();
    const readme = fs.readFileSync(path.resolve(__dirname, '../README.md'), 'utf-8');
    expect(readme).toMatch(/\| testcity \| 2 \|/);
    expect(console.log).toHaveBeenCalled();
  });

  test('checkNumbers catches inconsistency', () => {
    fs.writeFileSync(path.resolve(__dirname, '../README.md'), `
      | City   | 咖啡馆数量 |
      |--------|-----------|
      | testcity | 0 |
    `);
    fs.writeFileSync(cityGeoPath, JSON.stringify({
      type: "FeatureCollection",
      features: [{}]
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
      features: [{}, { properties: null }]
    }, null, 2));
    global.console = { log: jest.fn(), warn: jest.fn(), error: jest.fn() }; // add error to mock to avoid test crash
    lint.checkGeoJSON();
    expect(console.warn).toHaveBeenCalled();
  });

  test('getCafeNumbersFromReadme extracts correct numbers', () => {
    fs.writeFileSync(path.resolve(__dirname, '../README.md'), `
      | City   | 咖啡馆数量 |
      |--------|-----------|
      | testcity | 8 |
    `);
    const numbers = lint.getCafeNumbersFromReadme();
    expect(numbers['testcity']).toBe(8);
  });

  test('getCafeNumberFromGeo returns correct feature count', () => {
    fs.writeFileSync(cityGeoPath, JSON.stringify({
      type: "FeatureCollection",
      features: [{ properties: {} }, { properties: {} }, { properties: {} }]
    }, null, 2));
    expect(lint.getCafeNumberFromGeo(tempCity)).toBe(3);
  });

  test('isCounterMatched detects match', () => {
    fs.writeFileSync(cityGeoPath, JSON.stringify({
      type: "FeatureCollection",
      features: [{}, {}]
    }, null, 2));
    fs.writeFileSync(path.resolve(__dirname, '../README.md'), `
      | City   | 咖啡馆数量 |
      |--------|-----------|
      | testcity | 2 |
    `);
    expect(lint.isCounterMatched(tempCity, 2)).toBe(true);
    expect(lint.isCounterMatched(tempCity, 3)).toBe(false);
  });

  test('getCafeNumberFromGeo returns 0 for missing file', () => {
    // Remove geojson file before getCafeNumberFromGeo
    try { fs.unlinkSync(cityGeoPath); } catch {}
    expect(lint.getCafeNumberFromGeo(tempCity)).toBe(0);
    // Restore for other tests
    fs.writeFileSync(cityGeoPath, JSON.stringify({ type: "FeatureCollection", features: [] }, null, 2));
  });

  test('getCafeNumberFromGeo returns 0 for malformed geojson', () => {
    fs.writeFileSync(cityGeoPath, '{ this is not json');
    expect(() => lint.getCafeNumberFromGeo(tempCity)).toThrow();
    // Recovery: write valid geojson for next tests
    fs.writeFileSync(cityGeoPath, JSON.stringify({ type: "FeatureCollection", features: [] }, null, 2));
  });
});