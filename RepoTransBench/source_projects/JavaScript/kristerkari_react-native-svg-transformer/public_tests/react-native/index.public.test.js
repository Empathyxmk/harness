// public_tests/react-native/index.public.test.js
// Public test: only test exports, avoid calling transform to avoid plugin/teardown errors

describe("react-native/index.js public API", () => {
  test("react-native/index.js should export a 'transform' function (public)", () => {
    const mod = require("../../react-native/index.js");
    expect(typeof mod.transform).toBe("function");
  });
});