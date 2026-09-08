const { prefixNegativeModifiers } = require('./index');

describe("prefixNegativeModifiers", () => {
  it("is defined if exported", () => {
    expect(typeof prefixNegativeModifiers).toBe("function");
  });

  it("returns object unchanged when values are not numbers/strings", () => {
    const out = prefixNegativeModifiers({ foo: true, bar: null });
    expect(out).toEqual({ foo: true, bar: null });
  });

  it("adds prefix to negative number values", () => {
    const out = prefixNegativeModifiers({ a: -1, b: 2 });
    expect(out).toEqual({ a: "-1", b: "2" });
  });

  it("adds prefix to negative string numbers", () => {
    const out = prefixNegativeModifiers({ a: "-5", b: "1" });
    expect(out).toEqual({ a: "-5", b: "1" });
  });

  it("handles empty object", () => {
    expect(prefixNegativeModifiers({})).toEqual({});
  });

  it("handles zero and strings with minus", () => {
    expect(prefixNegativeModifiers({ a: 0, b: "-0", c: -0 })).toEqual({ a: "0", b: "-0", c: "0" });
  });
});