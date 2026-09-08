const jsdocParse = require('../');
const transform = require('../lib/transform');
const sortArray = require('sort-array');

// Minimal fixture for transform test
const sampleInput = [
  {
    name: "module:someModule",
    longname: "module:someModule",
    kind: "function",
    meta: { code: { name: "doThing" } }
  },
  {
    name: "SomeClass",
    longname: "SomeClass",
    kind: "class",
    meta: { code: { name: "SomeClass" } }
  },
  {
    name: "module:exportedThing",
    longname: "module:exportedThing",
    kind: "member",
    meta: { code: { name: "exportedThing" } }
  },
  {
    name: "notExported",
    longname: "notExported",
    kind: "member"
  }
];

describe('index.js', () => {
  test('jsdocParse returns array sorted by scope, category, kind, order', () => {
    const input = [
      { name: "b", kind: "class", scope: "instance", order: 2, category: "x" },
      { name: "c", kind: "constant", scope: "global", order: 1, category: "a" },
      { name: "a", kind: "function", scope: "static", order: 0, category: "z" }
    ];
    // transform is identity; mocking to just pass input through so we can see sort
    jest.spyOn(require('../lib/transform'), 'apply').mockImplementation((d) => d);
    // Using the jsdocParse as a wrapper for sort here
    const result = require('../')(input);
    expect(Array.isArray(result)).toBe(true);
    expect(result[0]).toHaveProperty('name');
    expect(result.length).toBe(3);

    // Order should be sorted based on index.js's sort() rules
    expect(result.map(i => i.name)).toEqual(['c', 'b', 'a']);
  });

  test('jsdocParse runs transform and sorting', () => {
    const data = JSON.parse(JSON.stringify(sampleInput));
    const output = jsdocParse(data);
    expect(Array.isArray(output)).toBe(true);
    expect(output.length).toBeGreaterThan(0);
    // Exported member will get special id
    expect(output.some(d => d.isExported)).toBe(true);
  });
});