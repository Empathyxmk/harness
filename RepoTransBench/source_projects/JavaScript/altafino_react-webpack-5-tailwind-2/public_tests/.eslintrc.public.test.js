describe(".eslintrc.js (public)", () => {
  it("should export required keys and at least one plugin", () => {
    const config = require("../.eslintrc.js");
    expect(config).toHaveProperty('env');
    expect(config).toHaveProperty('parser');
    expect(config).toHaveProperty('extends');
    expect(Array.isArray(config.extends)).toBe(true);
    expect(typeof config.rules).toBe("object");
    expect(config).toHaveProperty('plugins');
    expect(Array.isArray(config.plugins)).toBe(true);
    expect(config.plugins.length).toBeGreaterThan(0); // Test on length instead of content
    expect(config).toHaveProperty('settings');
  });

  it("should have 'react' as the first plugin (if present), or in the list", () => {
    const config = require("../.eslintrc.js");
    if (config.plugins.length > 0) {
      expect(config.plugins[0] === "react" || config.plugins.includes("react")).toBe(true);
    }
  });
});