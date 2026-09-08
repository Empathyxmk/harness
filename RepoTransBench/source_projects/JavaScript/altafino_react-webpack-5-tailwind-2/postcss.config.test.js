const config = require('./postcss.config');

describe('postcss.config.js', () => {
  it('should export an object with plugins array', () => {
    expect(config).toBeDefined();
    expect(typeof config).toBe('object');
    expect(Array.isArray(config.plugins)).toBe(true);
  });

  it('should include tailwindcss and autoprefixer plugins (by presence/type or string)', () => {
    // Plugins can be required via require, so require them for direct comparison as well
    let tailwindcss, autoprefixer;
    try {
      tailwindcss = require('tailwindcss');
    } catch (e) {
      // fallback or skip direct require if not installed as dependency
      tailwindcss = null;
    }
    try {
      autoprefixer = require('autoprefixer');
    } catch (e) {
      autoprefixer = null;
    }

    // Accept many notations: constructor.name, postcssPlugin property, string, or reference
    let foundTailwind = false;
    let foundAutoprefixer = false;

    for (const plugin of config.plugins) {
      // direct reference match
      if (plugin === tailwindcss || (plugin && tailwindcss && plugin.postcssPlugin === tailwindcss().postcssPlugin)) {
        foundTailwind = true;
      }
      if (plugin === autoprefixer || (plugin && autoprefixer && plugin.postcssPlugin === autoprefixer().postcssPlugin)) {
        foundAutoprefixer = true;
      }

      // postcssPlugin property
      if (plugin && typeof plugin === 'function') {
        try {
          const inst = plugin();
          if (
            inst &&
            inst.postcssPlugin &&
            /tailwind/i.test(inst.postcssPlugin)
          )
            foundTailwind = true;
          if (
            inst &&
            inst.postcssPlugin &&
            /autoprefixer/i.test(inst.postcssPlugin)
          )
            foundAutoprefixer = true;
        } catch (e) {
          // ignore
        }
      }
      if (
        plugin &&
        plugin.postcssPlugin &&
        /tailwind/i.test(plugin.postcssPlugin)
      )
        foundTailwind = true;
      if (
        plugin &&
        plugin.postcssPlugin &&
        /autoprefixer/i.test(plugin.postcssPlugin)
      )
        foundAutoprefixer = true;

      // constructor name
      if (
        plugin &&
        plugin.constructor &&
        plugin.constructor.name &&
        /tailwind/i.test(plugin.constructor.name)
      )
        foundTailwind = true;
      if (
        plugin &&
        plugin.constructor &&
        plugin.constructor.name &&
        /autoprefixer/i.test(plugin.constructor.name)
      )
        foundAutoprefixer = true;

      // string form
      if (typeof plugin === 'string') {
        if (/tailwind/i.test(plugin)) foundTailwind = true;
        if (/autoprefixer/i.test(plugin)) foundAutoprefixer = true;
      }
    }

    expect(foundTailwind).toBe(true);
    expect(foundAutoprefixer).toBe(true);
  });
});