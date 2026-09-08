const encode = require('../encode');
const decode = require('../decode');

// Helper to check encoding result while ignoring key order
function splitSort(str) {
  return str.split('&').sort().join('&');
}

describe("encode basic cases (public)", () => {
  test("should encode object with different URL special characters (public)", () => {
    // Only check for the result that matches what encode produces (all non-alphabetic non-digit chars encoded)
    expect(encode({ search: "baz qux", weird: "^~," })).toBe(
      "search=baz%20qux&weird=%5E~%2C"
    );
    // Also, test some that should be encoded (space, %, =, +, ;, /)
    expect(encode({ path: "foo/bar", percent: "%", plus: "+" })).toBe("path=foo%2Fbar&percent=%25&plus=%2B");
  });

  test("should encode empty object as empty string (public)", () => {
    expect(encode({})).toBe("");
  });

  test("should encode numeric keys and values (public)", () => {
    // Accept either key order
    const result = encode({ 120: 555, 88: 1234 });
    const expected1 = "120=555&88=1234";
    const expected2 = "88=1234&120=555";
    expect(result === expected1 || result === expected2).toBe(true);
  });

  test("should encode null & undefined as empty (public)", () => {
    // Accept either key order
    const result = encode({ foo: null, bar: undefined, xyz: 'z' });
    const parts = result.split('&').sort();
    expect(parts).toEqual(["bar=","foo=","xyz=z"].sort());
  });

  test("should encode multiple types (public)", () => {
    // Arrays produce repeating keys
    const result = encode({ bool: true, arr: [7, "m"], str: "zxy" });
    // arr can be either order, and overall key order can vary
    const options = [
      "bool=true&arr=7&arr=m&str=zxy",
      "bool=true&arr=m&arr=7&str=zxy",
      "arr=7&arr=m&bool=true&str=zxy",
      "arr=m&arr=7&bool=true&str=zxy",
      "str=zxy&bool=true&arr=7&arr=m",
      "str=zxy&bool=true&arr=m&arr=7"
    ];
    expect(options).toContain(result);
  });
});

describe("decode basic cases (public)", () => {
  test("should decode string to object (public)", () => {
    expect(decode("lat=42&lon=73")).toEqual({lat: "42", lon: "73"});
  });

  test("should decode percent-encoded values (public)", () => {
    expect(decode("greeting=hi%21")).toEqual({greeting: "hi!"});
  });

  test("should decode multiple with same key (public)", () => {
    expect(decode("value=a&value=b&value=c")).toEqual({value: ["a","b","c"]});
  });

  test("should decode empty string as empty object (public)", () => {
    expect(decode("")).toEqual({});
  });

  test("should decode null and missing values as empty string (public)", () => {
    // Order of keys may not matter, so just check obj equivalence
    const obj = decode("empty&set=");
    expect(obj).toEqual({empty: "", set: ""});
  });

  test("should decode encoded reserved chars (public)", () => {
    expect(decode("symbols=%24%40%5E")).toEqual({symbols: "$@^"});
  });
});