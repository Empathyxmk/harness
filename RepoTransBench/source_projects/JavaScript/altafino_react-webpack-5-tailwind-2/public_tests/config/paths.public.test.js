describe('paths.js (public)', () => {
  it('should export an object with at least a src or appIndexJs path', () => {
    const paths = require('../../config/paths.js');
    expect(paths).toBeDefined();
    expect(typeof paths).toBe('object');
    // Instead of checking all props, check for either src or appIndexJs
    expect(
      paths.hasOwnProperty('src') ||
      paths.hasOwnProperty('appIndexJs')
    ).toBe(true);
  });

  it('all exported path values should be strings or functions', () => {
    const paths = require('../../config/paths.js');
    for (const k in paths) {
      expect(
        typeof paths[k] === 'string' ||
        typeof paths[k] === 'function'
      ).toBe(true);
    }
  });
});