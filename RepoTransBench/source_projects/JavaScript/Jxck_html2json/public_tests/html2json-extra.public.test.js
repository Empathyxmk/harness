const { html2json, json2html } = require('../src/html2json');

// Test doctype and xml header removal (different tag and text)
describe('removeDOCTYPE - public', () => {
  it('removes xml and doctype headers with body tag', () => {
    const html = '<?xml version="1.1"?>\n<!DOCTYPE html>\n<body>public</body>';
    const json = html2json(html);
    expect(json.child[0].tag).toBe('body');
    expect(json.child[0].child[0].text).toBe('public');
  });
});

// Test element with multiple attributes and spaces (different tag/attr values)
describe('Attribute handling - public', () => {
  it('parses attributes with multiword values as arrays (different value)', () => {
    const html = '<meta name="keywords" content="foo bar baz">';
    const json = html2json(html);
    expect(Array.isArray(json.child[0].attr.content)).toBe(true);
    expect(json.child[0].attr.content).toEqual(['foo bar', 'baz']);
  });

  it('merges duplicate class attrs into array (different class/href value)', () => {
    const testJson = {
      node: 'element',
      tag: 'span',
      attr: {
        class: ['alpha', 'beta'],
        href: 'https://example.com'
      }
    };
    expect(json2html(testJson)).toContain('class="alpha beta"');
    expect(json2html(testJson)).toContain('href="https://example.com"');
  });
});

// Test empty element output (different tag & attr)
describe('json2html empty tag - public', () => {
  it('outputs self-closing tag if in empty list with br', () => {
    const json = {
      node: 'element', tag: 'br', attr: { id: 'break1' }
    };
    expect(json2html(json)).toBe('<br id="break1"/>');
  });
});

// Test rendering with no attr/child (different minimal tag)
describe('json2html minimal - public', () => {
  it('renders element with no attr or child (i tag)', () => {
    const json = { node: 'element', tag: 'i' };
    expect(json2html(json)).toBe('<i></i>');
  });
});

// Text and comment nodes in json2html (different text)
describe('Special nodes - public', () => {
  it('renders text node as text (xyz)', () => {
    const json = { node: 'text', text: 'xyz' };
    expect(json2html(json)).toBe('xyz');
  });

  it('renders comment nodes properly (another comment)', () => {
    const json = { node: 'comment', text: 'another comment' };
    expect(json2html(json)).toBe('<!--another comment-->');
  });
});

// Error/edge handling in html2json (different mismatch tags)
describe('html2json tag mismatch - public', () => {
  it('should handle mismatched tag (span/div) without error', () => {
    expect(() => html2json('<span></div>')).not.toThrow();
  });
});

// Deeply nested structure (different tags/count)
describe('Complex structure - public', () => {
  it('parses differently nested structure', () => {
    const html = '<section><ol><li>a</li><li>b</li></ol></section>';
    const json = html2json(html);
    expect(json.child[0].tag).toBe('section');
    expect(json.child[0].child[0].tag).toBe('ol');
    expect(json.child[0].child[0].child.length).toBe(2);
  });
});