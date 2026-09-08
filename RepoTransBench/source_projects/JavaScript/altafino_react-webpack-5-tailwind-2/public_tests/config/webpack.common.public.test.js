describe('webpack.common.js (public)', () => {
  it('should export an object and have a module.rules array', () => {
    const config = require('../../config/webpack.common.js');
    expect(config).toBeDefined();
    expect(typeof config).toBe('object');
    expect(config.module).toBeDefined();
    expect(Array.isArray(config.module.rules)).toBe(true);
    expect(config.module.rules.length).toBeGreaterThanOrEqual(1); // Require at least one rule
  });

  it('should have resolve.extensions as an array', () => {
    const config = require('../../config/webpack.common.js');
    expect(config.resolve).toBeDefined();
    expect(Array.isArray(config.resolve.extensions)).toBe(true);
  });
});