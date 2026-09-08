const objectsToCsv = require('../index');

describe('objectsToCsv (public)', () => {
  it('should throw if input is not an array', () => {
    expect(() => objectsToCsv(null)).toThrow();
    expect(() => objectsToCsv(0)).toThrow();
    expect(() => objectsToCsv(true)).toThrow();
    expect(() => objectsToCsv('array')).toThrow();
  });

  it('should return empty string for empty array', () => {
    expect(objectsToCsv([])).toBe("");
  });

  it('should generate CSV with header and all keys (public data)', () => {
    const arr = [
      { name: "Alice", age: 30 },
      { name: "Bob", age: 25 }
    ];
    expect(objectsToCsv(arr)).toBe('"name","age"\nAlice,30\nBob,25');
  });

  it('should include all fields found in any object (public data)', () => {
    const arr = [
      { animal: "cat", color: "black" },
      { animal: "dog", tail: true }
    ];
    // Order of fields: animal, color, tail
    expect(objectsToCsv(arr)).toBe('"animal","color","tail"\ncat,black,\ndog,,true');
  });

  it('should allow specifying fields option (public data)', () => {
    const arr = [{ id: 5, a: "x", b: "y" }];
    expect(objectsToCsv(arr, { fields: ['b', 'id'] })).toBe('"b","id"\ny,5');
  });

  it('should escape delimiter, quotes, and newlines properly (public data)', () => {
    const arr = [
      { description: 'text,with,comma', info: 'info' },
      { description: 'has"doublequote', info: "multi\nline" },
      { description: "foo", info: "bar" }
    ];
    const csv = objectsToCsv(arr, { fields: ['description', 'info'] });
    expect(csv).toBe('"description","info"\n"text,with,comma",info\n"has""doublequote","multi\nline"\nfoo,bar');
  });

  it('should allow custom delimiter (public data)', () => {
    const arr = [
      { x: 100, y: 200 }
    ];
    expect(objectsToCsv(arr, { delimiter: '|' })).toBe('"x"|"y"\n100|200');
  });

  it('should not include header if header option is false (public data)', () => {
    const arr = [
      { first: 'A', second: 'B' }
    ];
    const csv = objectsToCsv(arr, { header: false });
    expect(csv).toBe('A,B');
  });

  it('should handle null/undefined properties as empty fields (public data)', () => {
    const arr = [
      { foo: null, bar: undefined, baz: 42 }
    ];
    expect(objectsToCsv(arr)).toBe('"foo","bar","baz"\n,,42');
  });
});