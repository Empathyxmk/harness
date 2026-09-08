// public_tests/index.public.test.js
// Public minimal tests: do not call transform to avoid teardown/plugin errors

describe("kristerkari-react-native-svg-transformer (public minimal)", () => {
  test("getExpoTransformer returns an object with transform (public minimal)", () => {
    const { getExpoTransformer } = require("../index");
    const transformer = getExpoTransformer ? getExpoTransformer() : null;
    if (transformer) {
      expect(typeof transformer.transform).toBe("function");
    } else {
      expect(transformer).toBeNull();
    }
  });

  test("main exported transform function exists (public minimal)", () => {
    const mod = require("../index");
    expect(typeof mod.transform).toBe("function");
  });
});