describe('tailwind.config.js', () => {
  it('should export expected structure', () => {
    const config = require('./tailwind.config.js');
    expect(config).toHaveProperty('purge');
    expect(config).toHaveProperty('darkMode');
    expect(config).toHaveProperty('theme');
    expect(config).toHaveProperty('variants');
    expect(config).toHaveProperty('plugins');
    expect(Array.isArray(config.plugins)).toBe(true);
    expect(typeof config.theme).toBe('object');
    expect(typeof config.variants).toBe('object');
  });
  it('should have darkMode as either false, "media" or "class"', () => {
    const config = require('./tailwind.config.js');
    expect(['media', 'class', false]).toContain(config.darkMode);
  });
});