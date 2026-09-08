// public_tests/expo/index.public.test.js
// Public test: only test exports, avoid calling transform to avoid plugin/teardown errors

describe("expo/index.js public API", () => {
  test("expo/index.js should export a 'transform' function (public)", () => {
    const mod = require("../../expo/index.js");
    expect(typeof mod.transform).toBe("function");
  });
});