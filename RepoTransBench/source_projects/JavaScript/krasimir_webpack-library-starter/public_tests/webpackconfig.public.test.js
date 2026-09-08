// Public test for webpack.config.js with more fields
describe('WEBPACK CONFIG PUBLIC: Extended config shape and dev mode test', () => {
  it('should contain the devtool property and it should be a string', () => {
    const config = require('../webpack.config.js');
    expect(config).toHaveProperty('devtool');
    expect(typeof config.devtool).toBe('string');
  });

  it('should have output.libraryTarget equal to "umd" by default', () => {
    const config = require('../webpack.config.js');
    expect(config.output.libraryTarget).toBe('umd');
    expect(config.entry.endsWith('/src/index.js')).toBeTruthy();
    expect(['development', 'production']).toContain(config.mode);
  });
});