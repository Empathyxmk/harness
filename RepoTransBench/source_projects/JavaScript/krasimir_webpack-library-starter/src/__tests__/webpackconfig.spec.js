// Node require test for webpack.config.js; no assertions, smoke test
describe('webpack.config.js', () => {
  it('should be able to require without error', () => {
    const config = require('../../webpack.config.js');
    expect(typeof config).toBe('object');
    expect(config).toHaveProperty('mode');
    expect(config).toHaveProperty('entry');
    expect(config).toHaveProperty('output');
  });

  it('should handle env=build and amd flag correctly', () => {
    // Mock process.argv for yargs
    const originalArgv = process.argv.slice();
    process.argv.push('--env=build', '--amd');
    jest.resetModules();
    const configBuild = require('../../webpack.config.js');
    expect(configBuild.mode).toBe('production');
    expect(configBuild.output.filename).toMatch(/\.amd\.min\.js$/);
    process.argv = originalArgv;
  });
});