const transform = require('../lib/transform');

describe('transform internals - partial branch/line coverage', () => {
  test('setCodename does nothing if no meta.code', () => {
    const doclet = {name: "NoMeta"};
    expect(transform.setCodename(doclet)).toBe(doclet);
  });

  test('setID fallback', () => {
    const d = {kind:"member"};
    expect(transform.setID(d)).toBe(d);
    // id not set if no longname
    expect(d.id).toBeUndefined();
  });

  test('setIsExportedFlag false for module/kind', () => {
    const d1 = {name: "module:x", kind: "module"};
    const d2 = {name: "module:x", kind: "constructor"};
    expect(transform.setIsExportedFlag(d1).isExported).toBeUndefined();
    expect(transform.setIsExportedFlag(d2).isExported).toBeUndefined();
  });

  test('createConstructor success', () => {
    const classDoclet = {
      kind: "class",
      longname: "Foo",
      name: "Foo",
      description: "something",
      params: [],
      examples: [],
      returns: [],
      exceptions: [],
      classdesc: "The class!"
    };
    const result = transform.createConstructor(classDoclet);
    expect(Array.isArray(result)).toBe(true);
    expect(result[0].kind).toBe("class");
    expect(result[1].kind).toBe("constructor");
    expect(result[0].description).toBe("The class!");
    expect(result[0].classdesc).toBeUndefined();
  });
});