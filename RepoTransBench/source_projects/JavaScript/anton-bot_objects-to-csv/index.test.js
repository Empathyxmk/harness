const objectsToCsv = require('./index');

describe('objectsToCsv', () => {
  it('should throw if input is not an array', () => {
    expect(() => objectsToCsv(undefined)).toThrow();
    expect(() => objectsToCsv({})).toThrow();
    expect(() => objectsToCsv('str')).toThrow();
    expect(() => objectsToCsv(123)).toThrow();
  });

  it('should return empty string for empty array', () => {
    expect(objectsToCsv([])).toBe("");
  });

  it('should generate CSV with header and all keys', () => {
    const arr = [
      { a: 1, b: 2 },
      { a: 3, b: 4 }
    ];
    expect(objectsToCsv(arr)).toBe('"a","b"\n1,2\n3,4');
  });

  it('should include all fields found in any object', () => {
    const arr = [
      { a: 1, b: 2 },
      { a: 3, c: 5 }
    ];
    // Order of fields: a,b,c
    expect(objectsToCsv(arr)).toBe('"a","b","c"\n1,2,\n3,,5');
  });

  it('should allow specifying fields option', () => {
    const arr = [{ x: 1, y: 2, z: 3 }];
    expect(objectsToCsv(arr, { fields: ['z', 'x'] })).toBe('"z","x"\n3,1');
  });

  it('should escape delimiter, quotes, and newlines properly', () => {
    const arr = [
      { text: 'val,1', text2: 'plain' },
      { text: 'with"quote', text2: "new\nline" },
      { text: "reg", text2: "norm" }
    ];
    const csv = objectsToCsv(arr, { fields: ['text', 'text2'] });
    expect(csv).toBe('"text","text2"\n"val,1",plain\n"with""quote","new\nline"\nreg,norm');
  });

  it('should allow custom delimiter', () => {
    const arr = [
      { a: 1, b: 2 }
    ];
    expect(objectsToCsv(arr, { delimiter: ';' })).toBe('"a";"b"\n1;2');
  });

  it('should not include header if header option is false', () => {
    const arr = [
      { one: 1, two: 2 }
    ];
    const csv = objectsToCsv(arr, { header: false });
    expect(csv).toBe('1,2');
  });

  it('should handle null/undefined properties as empty fields', () => {
    const arr = [
      { a: null, b: undefined, c: 7 }
    ];
    expect(objectsToCsv(arr)).toBe('"a","b","c"\n,,7');
  });
});