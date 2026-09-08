const transform = require('../lib/transform');

// Utilities for quick fixture
function buildDoclet(overrides) {
  return Object.assign({
    name: "SomeName",
    longname: "SomeLongName",
    kind: "member",
    meta: { code: { name: "SomeName" } }
  }, overrides);
}

describe('transform.js', () => {
  test('transform() strips undocumented, package, file', () => {
    const input = [
      { kind: 'file' },
      { kind: 'package' },
      { kind: 'module', undocumented: true },
      buildDoclet(),
    ];
    const output = transform(input);
    // Only the good doclet survives
    expect(output.length).toBe(1);
    expect(output[0].kind).toBe('member');
  });

  test('setIsExportedFlag flags exports', () => {
    const doclet = buildDoclet({ name: "module:foo", kind: "member" });
    transform.setIsExportedFlag(doclet);
    expect(doclet.isExported).toBe(true);
    expect(doclet.memberof).toBe(doclet.longname);
  });

  test('setCodename sets correct codeName', () => {
    const doclet = buildDoclet({});
    transform.setCodename(doclet);
    expect(doclet.codeName).toBe("SomeName");
  });

  test('setID with exported', () => {
    const doclet = buildDoclet({ longname: "foo", kind: "member", isExported: true, codeName: "bar" });
    transform.setID(doclet);
    expect(doclet.id).toBe("foo--bar");
  });

  test('setID with constructor and static', () => {
    const doclet = buildDoclet({ longname: "abc", kind: "constructor", scope: "static" });
    transform.setID(doclet);
    expect(doclet.id).toBe("abc");
    expect(doclet.scope).toBe(undefined);
  });

  test('setID with constructor and instance', () => {
    const doclet = buildDoclet({ longname: "def", kind: "constructor", scope: "instance" });
    transform.setID(doclet);
    expect(doclet.id).toBe("def()");
  });

  test('createConstructor throws on non-class', () => {
    const doclet = buildDoclet({ kind: "function" });
    expect(() => transform.createConstructor(doclet)).toThrow(/only pass a class/);
  });
});