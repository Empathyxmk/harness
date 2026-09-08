const fs = require('fs');
const path = require('path');

// To avoid jest.mock() using out-of-scope variables, mocks must use only globals or function-scoped variables in their factories!

const mockCities = ['unittestcity'];
const mockGeoPath = path.resolve(__dirname, `../unittestcity.geojson`);

jest.mock('./utils', () => {
  const path = require('path');
  return {
    GEOJSON_EXT: '.geojson',
    ROOT_DIR: path.resolve(__dirname, '..'),
    cities: mockCities,
    getCityGeoJSON: (city) => path.resolve(__dirname, `../${city}.geojson`)
  };
});

jest.mock('./lint', () => ({
  updateCafeNumbers: jest.fn()
}));

const markerColors = {
  GRAY: '#BEBEBE',
  RED: '#C24740',
  YELLOW: '#F3AE1A',
  GREEN: '#50C240',
};

describe('housekeeper.js', () => {
  beforeAll(() => {
    // Write a valid geojson file with mixed types for coverage
    fs.writeFileSync(
      mockGeoPath,
      JSON.stringify({
        type: 'FeatureCollection',
        features: [
          // Single value (RED)
          { properties: { "下载速度": "2.5 Mbps", "营业状态": "营业" } },
          // Array (YELLOW)
          { properties: { "下载速度": ["5.0 Mbps", "7.5 Mbps"], "营业状态": "营业" } },
          // Array (GREEN)
          { properties: { "下载速度": ["12 Mbps", "15 Mbps"], "营业状态": "营业" } },
          // Stopped (GRAY)
          { properties: { "下载速度": "10 Mbps", "营业状态": "停业" } },
        ]
      }, null, 2)
    );
  });

  afterAll(() => {
    fs.unlinkSync(mockGeoPath);
  });

  test('run buildMarker - marker colors and symbols are set correctly', () => {
    let outputData = '';
    const oldLog = console.log;
    console.log = function (...args) {
      outputData += args.join(' ') + '\n';
    };
    jest.resetModules();
    require('./housekeeper.js'); // This runs buildMarker and updateCafeNumbers

    const data = JSON.parse(fs.readFileSync(mockGeoPath, 'utf-8'));
    expect(data.features.length).toBe(4);

    expect(data.features[0].properties['marker-color']).toBe(markerColors.RED);
    expect(data.features[1].properties['marker-color']).toBe(markerColors.YELLOW);
    expect(data.features[2].properties['marker-color']).toBe(markerColors.GREEN);
    expect(data.features[3].properties['marker-color']).toBe(markerColors.GRAY);

    for (const feat of data.features) {
      expect(feat.properties['marker-symbol']).toBe('cafe');
    }
    expect(outputData).toMatch(/unittestcity: Done with 4 records!/);
    oldLog(outputData);
  });

  test('should throw error for invalid 下载速度', () => {
    // Put a speed string that does NOT match regex
    fs.writeFileSync(
      mockGeoPath,
      JSON.stringify({
        type: 'FeatureCollection',
        features: [
          { properties: { "下载速度": "???", "营业状态": "营业" } }
        ]
      })
    );
    jest.resetModules();
    const logOrig = console.log;
    console.log = () => {};
    expect(() => require('./housekeeper.js')).toThrow();
    console.log = logOrig;
  });
});