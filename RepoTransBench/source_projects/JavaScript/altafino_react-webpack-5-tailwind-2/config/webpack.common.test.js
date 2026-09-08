describe("webpack.common.js", () => {
  it("should export an object or function", () => {
    const config = require("./webpack.common.js");
    expect(typeof config === "object" || typeof config === "function").toBe(true);
  });
});