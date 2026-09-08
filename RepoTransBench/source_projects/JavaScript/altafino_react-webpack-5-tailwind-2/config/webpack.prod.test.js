describe("webpack.prod.js", () => {
  it("should export an object or function", () => {
    const config = require("./webpack.prod.js");
    expect(typeof config === "object" || typeof config === "function").toBe(true);
  });
});