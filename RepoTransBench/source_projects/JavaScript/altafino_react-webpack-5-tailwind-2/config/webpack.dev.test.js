describe("webpack.dev.js", () => {
  it("should export an object or function", () => {
    const config = require("./webpack.dev.js");
    expect(typeof config === "object" || typeof config === "function").toBe(true);
  });
});