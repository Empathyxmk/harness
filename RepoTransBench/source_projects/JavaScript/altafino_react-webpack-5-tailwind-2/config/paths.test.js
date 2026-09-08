describe("config/paths.js", () => {
  let paths;
  beforeAll(() => {
    paths = require('./paths.js');
  });
  it("should be an object of paths", () => {
    expect(typeof paths).toBe("object");
    expect(Object.keys(paths).length).toBeGreaterThan(0);
  });
  it("should include at least one key with a path ending in src", () => {
    expect(
      Object.values(paths).some(path => typeof path === "string" && path.includes("src"))
    ).toBe(true);
  });
});