jest.mock("../index.js", () => {
  return {
    createTransformer: jest.fn(() => jest.fn(() => "rn transformed")),
    getReactNativeTransformer: jest.fn(() => ({ transform: jest.fn() }))
  };
});

test("react-native/index.js exports `.transform` via createTransformer(getReactNativeTransformer())", () => {
  const mod = require("./index.js");
  expect(typeof mod.transform).toBe("function");
  expect(mod.transform()).toBe("rn transformed");
});