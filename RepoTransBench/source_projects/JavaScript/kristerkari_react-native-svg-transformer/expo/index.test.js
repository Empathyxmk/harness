jest.mock("../index.js", () => {
  return {
    createTransformer: jest.fn(() => jest.fn(() => "expo transformed")),
    getExpoTransformer: jest.fn(() => ({ transform: jest.fn() }))
  };
});

test("expo/index.js exports `.transform` via createTransformer(getExpoTransformer())", () => {
  const mod = require("./index.js");
  expect(typeof mod.transform).toBe("function");
  expect(mod.transform()).toBe("expo transformed");
});