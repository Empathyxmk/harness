describe('webpack.prod.js (public)', () => {
  it('should export object and mode is "production"', () => {
    const config = require('../../config/webpack.prod.js');
    expect(config).toBeDefined();
    expect(typeof config).toBe('object');
    expect(config.mode).toEqual('production');
  });

  it('should have optimization.minimize set to true (public test: boolean check only)', () => {
    const config = require('../../config/webpack.prod.js');
    expect(config.optimization).toBeDefined();
    expect(typeof config.optimization.minimize).toBe('boolean');
  });
});