describe('webpack.dev.js (public)', () => {
  it('should export an object that has mode "development"', () => {
    const config = require('../../config/webpack.dev.js');
    expect(config).toBeDefined();
    expect(typeof config).toBe('object');
    expect(config.mode).toEqual('development');
  });

  it('should have devtool set and entry as a string or array', () => {
    const config = require('../../config/webpack.dev.js');
    expect(typeof config.devtool === 'string' || config.devtool === undefined).toBe(true);
    expect(
      typeof config.entry === 'string' ||
      Array.isArray(config.entry)
    ).toBe(true);
  });
});