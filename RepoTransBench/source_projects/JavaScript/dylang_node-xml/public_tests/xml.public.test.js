const xml = require('../lib/xml');

describe('xml main API (public)', () => {
  it('outputs string xml (different data)', () => {
    const str = xml({bar: 'baz'});
    expect(str).toBe('<bar>baz</bar>');
  });
  it('outputs array (different keys/values)', () => {
    const doc = [{one: 'uno'}, {two: 'dos'}];
    const str = xml(doc);
    expect(str).toBe('<one>uno</one><two>dos</two>');
  });
  it('accepts options.indent (different tag/attr)', () => {
    const doc = {greet: [{_attr: {lang: 'en'}}, 'hello']};
    const str = xml(doc, {indent: '  '});
    expect(typeof str).toBe('string');
    expect(str.startsWith('<greet lang="en">')).toBeTruthy();
    expect(str.endsWith('hello</greet>')).toBeTruthy();
  });
  it('accepts options.declaration (encoding changed)', () => {
    const doc = {xyz: 'qrs'};
    const str = xml(doc, {declaration: {encoding: 'ISO-8859-1'}});
    expect(str).toMatch(/encoding="ISO-8859-1"/);
  });
  it('accepts options.declaration (omit, different data)', () => {
    const doc = {hello: 'world'};
    const str = xml(doc, {declaration: false});
    expect(str.startsWith('<hello>')).toBeTruthy();
  });
  it('accepts options.standalone (public: just type check)', () => {
    const doc = {a: 'b'};
    const str = xml(doc, {declaration: {standalone: true}});
    expect(typeof str).toBe('string');
  });
  it('accepts options.version (public: still 1.0)', () => {
    const doc = {foo: 'bar'};
    const str = xml(doc, {declaration: {version: '2.0'}});
    expect(str).toContain('version="1.0"');
  });
  it('accepts options.stream and options.headless (different child)', done => {
    const elem = xml.Element({apples: 'red'});
    const stream = xml({fruits: elem}, {stream: true, headless: true, indent: ''});
    let results = [];
    stream.on('data', chunk => results.push(chunk));
    stream.on('end', () => {
      const xmlstr = results.join('');
      expect(xmlstr.startsWith('<fruits>')).toBeTruthy();
      expect(xmlstr.endsWith('</fruits>')).toBeTruthy();
      done();
    });
    elem.close();
  });
});