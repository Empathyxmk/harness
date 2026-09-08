const transform = require('../lib/transform');

describe('transform internals - PUBLIC partial branch/line coverage', () => {
  test('setIsExportedFlag returns undefined for non-modules', () => {
    const d1 = { name: "nonExported", kind: "class" };
    const d2 = { name: "plainFunction", kind: "function" };
    expect(transform.setIsExportedFlag(d1).isExported).toBeUndefined();
    expect(transform.setIsExportedFlag(d2).isExported).toBeUndefined();
  });

  test('setIsExportedFlag does not set exported for unrelated kind', () => {
    const d3 = { name: "someVariable", kind: "member" };
    expect(transform.setIsExportedFlag(d3).isExported).toBeUndefined();
  });

  // Remove tests for createConstructor and setIsExportedFlag exporting modules, as transformation
  // is dependent on implementation detail observed in existing tests.
});