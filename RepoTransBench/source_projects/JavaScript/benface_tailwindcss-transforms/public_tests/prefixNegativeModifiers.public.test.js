const { prefixNegativeModifiers } = require('../index');

describe("prefixNegativeModifiers (public)", () => {
  it("is defined if exported", () => {
    expect(typeof prefixNegativeModifiers).toBe("function");
  });

  it("returns object unchanged when values are arrays/objects", () => {
    const out = prefixNegativeModifiers({ foo: [42], bar: { a: 1 } });
    expect(out).toEqual({ foo: [42], bar: { a: 1 } });
  });

  it("adds prefix to different negative number values", () => {
    const out = prefixNegativeModifiers({ x: -10, y: 3 });
    expect(out).toEqual({ x: "-10", y: "3" });
  });

  it("adds prefix to other negative string numbers", () => {
    const out = prefixNegativeModifiers({ x: "-7", y: "9" });
    expect(out).toEqual({ x: "-7", y: "9" });
  });

  it("handles another empty object", () => {
    expect(prefixNegativeModifiers({})).toEqual({});
  });

  it("handles zero, negative zero and string negative zero", () => {
    expect(prefixNegativeModifiers({ x: 0, y: "-0", z: -0 })).toEqual({ x: "0", y: "-0", z: "0" });
  });
});