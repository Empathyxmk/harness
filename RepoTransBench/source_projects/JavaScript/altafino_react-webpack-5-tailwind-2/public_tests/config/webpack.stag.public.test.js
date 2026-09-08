describe('webpack.stag.js (public)', () => {
  it('should export object and mode should be "production" or "staging"', () => {
    const config = require('../../config/webpack.stag.js');
    expect(config).toBeDefined();
    expect(['production', 'staging']).toContain(config.mode);
  });
  it('should have output.path and output.filename defined', () => {
    const config = require('../../config/webpack.stag.js');
    expect(config.output).toBeDefined();
    expect(config.output.path).toBeDefined();
    expect(config.output.filename).toBeDefined();
  });
});