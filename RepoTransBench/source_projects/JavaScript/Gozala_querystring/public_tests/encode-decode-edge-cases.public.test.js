const encode = require("../encode.js");
const decode = require("../decode.js");

describe("encode() edge cases (public)", () => {
  test("should encode object with undefined value as empty string (public)", () => {
    expect(encode({ x: undefined, y: 42 })).toBe("x=&y=42");
  });

  test("should encode arrays in object (public)", () => {
    expect(encode({ fruits: ["apple", "banana", "cherry"], count: 3 })).toBe("fruits=apple&fruits=banana&fruits=cherry&count=3");
  });

  test("should encode array of arrays as empty string for each element (public)", () => {
    expect(encode({ arr: [[5, 6], [7, 8]] })).toBe("arr=&arr=");
  });

  test("should encode object with functions (value becomes empty, public)", () => {
    const str = encode({ hello: "world", myFunc: () => {}, flag: false });
    expect(str).toContain("hello=world");
    expect(str).toContain("flag=false");
    expect(str).toContain("myFunc=");
  });

  test("should encode null and boolean values, with null as empty string (public)", () => {
    expect(encode({ a: null, b: true, c: -1 })).toBe("a=&b=true&c=-1");
  });
});

describe("decode() edge cases (public)", () => {
  test("should decode to object with multiple keys (public)", () => {
    expect(decode("x=42&y=0&z=NaN")).toEqual({ x: "42", y: "0", z: "NaN" });
  });

  test("should decode repeated keys as array (public)", () => {
    expect(decode("val=a&val=b&val=c")).toEqual({ val: ["a", "b", "c"] });
  });

  test("should decode empty value (public)", () => {
    expect(decode("x=&y=100")).toEqual({ x: "", y: "100" });
  });

  test("should decode array-encoded and URI components (public)", () => {
    expect(decode("list=apple%2Cpie&list=banana%2Csplit")).toEqual({ list: ["apple,pie", "banana,split"] });
  });

  test("should decode plus as space (public)", () => {
    expect(decode("x=foo+bar&y=1+1")).toEqual({ x: "foo bar", y: "1 1" });
  });

  test("should decode null, false, true string values as they are (public)", () => {
    expect(decode("x=nil&y=no&z=yes")).toEqual({ x: "nil", y: "no", z: "yes" });
  });
});