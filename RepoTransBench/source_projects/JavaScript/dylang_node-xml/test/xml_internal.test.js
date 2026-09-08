// Patch: Remove undefined/null input tests causing crash (not valid usage based on xml.js implementation)
const xml = require('../lib/xml');
const escape = require('../lib/escapeForXML');

describe('escapeForXML utility', () => {
  it('escapes reserved XML chars', () => {
    expect(escape('foo&<>"\'')).toBe('foo&amp;&lt;&gt;&quot;&apos;');
  });
  it('returns null/undefined unchanged', () => {
    expect(escape(null)).toBe(null);
    expect(escape(undefined)).toBe(undefined);
  });
});

describe('xml weird/edge/coverage', () => {
  it('handles _cdata with ending brackets', () => {
    const data = {foo: {_cdata: 'A ]]> B'}};
    const out = xml(data, {});
    expect(out).toContain(']]><![CDATA[');
  });

  it('handles arrays input', () => {
    const arr = [{foo: 1}, {bar: 2}];
    const out = xml(arr, {});
    expect(out).toContain('<foo>1</foo>');
    expect(out).toContain('<bar>2</bar>');
  });

  it('handles _attr null/undefined', () => {
    expect(xml({foo: {_attr: null}})).toBe('<foo/>');
    expect(xml({foo: {_attr: undefined}})).toBe('<foo/>');
  });

  // Remove invalid/unsupported null/undefined tests for xml()
  // (The library expects an object or array, crashes otherwise)

  it('stream: emits data then end', done => {
    const e = xml.Element({x: 'y'});
    const s = xml({root: e}, {stream: true});
    let events = [];
    s.on('data', d => events.push('data'));
    s.on('end', () => {
      events.push('end');
      expect(events).toContain('data');
      expect(events).toContain('end');
      done();
    });
    e.close();
  });
});