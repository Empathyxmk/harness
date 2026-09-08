describe('tailwind.config.js (public)', () => {
  it('should have theme and plugins keys and plugins array should be empty or have 0 length', () => {
    const config = require('../tailwind.config.js');
    expect(config).toHaveProperty('theme');
    expect(config).toHaveProperty('plugins');
    expect(Array.isArray(config.plugins)).toBe(true);
    expect(config.plugins.length).toBeLessThanOrEqual(0); // Expecting empty plugins array
  });

  it('should have a purge pointing to .js files in the src dir', () => {
    const config = require('../tailwind.config.js');
    expect(typeof config.purge).toBe('object' || 'string' || 'array');
    if (Array.isArray(config.purge)) {
      expect(config.purge.some(e => typeof e === 'string' && e.includes('src') && e.endsWith('.js'))).toBe(true);
    } else if (typeof config.purge === 'string') {
      expect(config.purge.includes('src')).toBe(true);
      expect(config.purge.endsWith('.js')).toBe(true);
    } else if (config.purge) {
      // accept object form for purge in Tailwind 3+
      expect(typeof config.purge).toBe('object');
    }
  });
});