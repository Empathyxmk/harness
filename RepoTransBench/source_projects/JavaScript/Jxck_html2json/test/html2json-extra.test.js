const { html2json, json2html } = require('../src/html2json');

// Test doctype and xml header removal
describe('removeDOCTYPE', () => {
  it('removes xml and doctype headers', () => {
    const html = '<?xml version="1.0"?>\n<!DOCTYPE html>\n<div>test</div>';
    const json = html2json(html);
    expect(json.child[0].tag).toBe('div');
    expect(json.child[0].child[0].text).toBe('test');
  });
});

// Test element with multiple attributes and spaces
describe('Attribute handling', () => {
  it('parses attributes with multiword values as arrays', () => {
    const html = '<meta name="viewport" content="width=device width">';
    const json = html2json(html);
    expect(Array.isArray(json.child[0].attr.content)).toBe(true);
    expect(json.child[0].attr.content).toEqual(['width=device', 'width']);
  });

  it('merges duplicate attrs into array', () => {
    // Should not happen in strict HTML, but let's create the scenario
    const testJson = {
      node: 'element',
      tag: 'a',
      attr: {
        class: ['foo', 'bar'],
        href: 'http://x.com'
      }
    };
    expect(json2html(testJson)).toContain('class="foo bar"');
    expect(json2html(testJson)).toContain('href="http://x.com"');
  });
});

// Test empty element output
describe('json2html empty tag', () => {
  it('outputs self-closing tag if in empty list', () => {
    const json = {
      node: 'element', tag: 'img', attr: { src: 'x.png' }
    };
    expect(json2html(json)).toBe('<img src="x.png"/>');
  });
});

// Test rendering with no attr/child
describe('json2html minimal', () => {
  it('renders element with no attr or child', () => {
    const json = { node: 'element', tag: 'b' };
    expect(json2html(json)).toBe('<b></b>');
  });
});

// Text and comment nodes in json2html
describe('Special nodes', () => {
  it('renders text node as text', () => {
    const json = { node: 'text', text: 'abc' };
    expect(json2html(json)).toBe('abc');
  });

  it('renders comment nodes properly', () => {
    const json = { node: 'comment', text: ' this ' };
    expect(json2html(json)).toBe('<!-- this -->');
  });
});

// Error/edge handling in html2json
describe('html2json tag mismatch', () => {
  it('should handle mismatched tag without error', () => {
    // The original code doesn't throw or output a global error,
    // so this just checks that it doesn't throw.
    expect(() => html2json('<div></span>')).not.toThrow();
  });
});

describe('Complex structure', () => {
  it('parses deeply nested structure', () => {
    const html = '<div><ul><li>1</li><li>2</li><li>3</li></ul></div>';
    const json = html2json(html);
    expect(json.child[0].tag).toBe('div');
    expect(json.child[0].child[0].tag).toBe('ul');
    expect(json.child[0].child[0].child.length).toBe(3);
  });
});