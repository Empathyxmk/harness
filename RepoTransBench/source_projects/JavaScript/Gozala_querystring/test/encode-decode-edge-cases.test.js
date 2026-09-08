const encode = require("../encode.js");
const decode = require("../decode.js");

describe("encode() edge cases", () => {
  test("should encode object with undefined value as empty string", () => {
    expect(encode({ a: undefined, b: 2 })).toBe("a=&b=2");
  });

  test("should encode arrays in object", () => {
    expect(encode({ a: [1, 2, 3], b: "ok" })).toBe("a=1&a=2&a=3&b=ok");
  });

  test("should encode array of arrays as empty string for each element", () => {
    // [[1,2],[3,4]] becomes [1,2].toString="1,2" and [3,4].toString="3,4"
    // But implementation may encode each sub-array as '', so expect empty values
    expect(encode({ arr: [[1, 2], [3, 4]] })).toBe("arr=&arr=");
  });

  test("should encode object with functions (value becomes empty)", () => {
    const str = encode({ a: "str", func: function () {}, b: true });
    expect(str).toContain("a=str");
    expect(str).toContain("b=true");
    // key with function value is encoded as key=
    expect(str).toContain("func=");
  });

  test("should encode null and boolean values, with null as empty string", () => {
    expect(encode({ a: null, b: false, c: 0 })).toBe("a=&b=false&c=0");
  });
});

describe("decode() edge cases", () => {
  test("should decode to object with multiple keys", () => {
    expect(decode("a=1&b=2&c=3")).toEqual({ a: "1", b: "2", c: "3" });
  });

  test("should decode repeated keys as array", () => {
    expect(decode("a=1&a=2&a=3")).toEqual({ a: ["1", "2", "3"] });
  });

  test("should decode empty value", () => {
    expect(decode("a=&b=2")).toEqual({ a: "", b: "2" });
  });

  test("should decode array-encoded and URI components", () => {
    expect(decode("arr=1%2C2&arr=3%2C4")).toEqual({ arr: ["1,2", "3,4"] });
  });

  test("should decode plus as space", () => {
    expect(decode("a=hello+world&b=1+2")).toEqual({ a: "hello world", b: "1 2" });
  });

  test("should decode null, false, true string values as they are", () => {
    expect(decode("a=null&b=false&c=true")).toEqual({ a: "null", b: "false", c: "true" });
  });
});