const encode = require("../encode.js");
const decode = require("../decode.js");

describe("encode basic cases", () => {
  test("should encode simple object", () => {
    expect(encode({ foo: "bar", baz: 1 })).toBe("foo=bar&baz=1");
  });

  test("should encode with special URL characters", () => {
    expect(encode({ q: "hello world", sym: "&=?"})).toBe("q=hello%20world&sym=%26%3D%3F");
  });

  test("should encode empty object as empty string", () => {
    expect(encode({})).toBe("");
  });
});

describe("decode basic cases", () => {
  test("should decode single pair", () => {
    expect(decode("a=1")).toEqual({ a: "1" });
  });

  test("should decode empty string as empty object", () => {
    expect(decode("")).toEqual({});
  });

  test("should decode keys with encoded characters", () => {
    expect(decode("q=hello%20world&sym=%26%3D%3F")).toEqual({ q: "hello world", sym: "&=?" });
  });

  test("should decode equals with missing value as empty string", () => {
    expect(decode("a=&b=")).toEqual({ a: "", b: "" });
  });
});