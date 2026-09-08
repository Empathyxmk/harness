const config = require('../postcss.config');

describe('postcss.config.js (public)', () => {
  it('should export an object and plugins array should have minimum 3 plugins', () => {
    expect(config).toBeDefined();
    expect(typeof config).toBe('object');
    expect(Array.isArray(config.plugins)).toBe(true);
    expect(config.plugins.length).toBeGreaterThanOrEqual(3); // Different property tested
  });

  it('should have the first plugin as postcss-import, and all entries are functions or strings', () => {
    // Slightly different check order: check for postcss-import at index 0 and types
    let postcssImport;
    try {
      postcssImport = require('postcss-import');
    } catch (e) {
      postcssImport = null;
    }
    const first = config.plugins[0];
    let firstIsImport = false;
    if (first === postcssImport) firstIsImport = true;
    if (typeof first === "function") {
      try {
        const inst = first();
        if (inst && inst.postcssPlugin && /import/i.test(inst.postcssPlugin)) {
          firstIsImport = true;
        }
      } catch (e) { }
    }
    if (typeof first === "string" && /import/i.test(first)) firstIsImport = true;

    expect(firstIsImport).toBe(true);

    config.plugins.forEach(p => expect(['function', 'string'].includes(typeof p)).toBe(true));
  });
});