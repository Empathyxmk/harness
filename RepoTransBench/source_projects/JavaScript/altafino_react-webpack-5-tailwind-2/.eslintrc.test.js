describe(".eslintrc.js", () => {
  it("should export an object with required properties", () => {
    const config = require("./.eslintrc.js");
    expect(config).toHaveProperty('env');
    expect(config).toHaveProperty('parser');
    expect(config).toHaveProperty('extends');
    expect(Array.isArray(config.extends)).toBe(true);
    expect(typeof config.rules).toBe("object");
    expect(config).toHaveProperty('plugins');
    expect(Array.isArray(config.plugins)).toBe(true);
    expect(config).toHaveProperty('settings');
  });

  it("should include react plugin", () => {
    const config = require("./.eslintrc.js");
    expect(config.plugins.includes('react')).toBe(true);
  });
});