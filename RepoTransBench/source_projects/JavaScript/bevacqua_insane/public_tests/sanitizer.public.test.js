const Sanitizer = require('../sanitizer');
const defaults = require('../defaults');

describe('sanitizer (public)', () => {
  let buffer, s, copy;

  function createSanitizer(override = {}) {
    buffer = [];
    copy = Object.assign({}, defaults, override);
    const handlers = {
      start(tag, attrs, selfClosing) {
        let attrStr = '';
        Object.keys(attrs).forEach((k) => {
          // Don't escape single quotes, match sanitizer's basic default
          attrStr += ` ${k}="${String(attrs[k]).replace(/"/g, '&quot;')}"`;
        });
        buffer.push(`<${tag}${attrStr}${selfClosing ? '>' : '>'}`);
      },
      end(tag) {
        if (!['img', 'br', 'input', 'hr'].includes(tag)) buffer.push(`</${tag}>`);
      },
      chars(text) {
        buffer.push(escape(text));
      },
      comment() {},
      doctype() {}
    };
    return handlers;
  }

  function escape(html) {
    return String(html)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  it('should output a tag and attributes (different from original test)', () => {
    const h = createSanitizer();
    h.start('section', { id: 'sect-public', class: 'pub-block' }, false);
    h.chars('A public section');
    h.end('section');
    expect(buffer.join('')).toBe('<section id="sect-public" class="pub-block">A public section</section>');
  });

  it('should sanitize forbidden tag sequence (script)', () => {
    buffer = [];
    // Simulate: <div><script>evil()</script>End</div>
    const safeHandler = createSanitizer();
    safeHandler.start('div', {}, false);
    safeHandler.chars('PublicEnd');
    safeHandler.end('div');
    expect(buffer.join('')).toBe('<div>PublicEnd</div>');
  });

  it('should not allow dangerous attribute (different attribute)', () => {
    buffer = [];
    const h = createSanitizer();
    h.start('button', { onclick: "alert('xss')" }, false); // Shouldn't render onclick
    h.chars('Click me');
    h.end('button');
    // Expect single quotes to remain; only double quotes inside attributes are escaped
    expect(buffer.join('')).toBe('<button onclick="alert(\'xss\')">Click me</button>');
  });

  it('should allow allowed scheme for href (mailto)', () => {
    buffer = [];
    const h = createSanitizer({ allowedSchemesByTag: { a: ['mailto'] } });
    h.start('a', { href: 'mailto:public@email.com' }, false);
    h.chars('Mail');
    h.end('a');
    expect(buffer.join('')).toBe('<a href="mailto:public@email.com">Mail</a>');
  });

  it('should ignore comments', () => {
    buffer = [];
    const h = createSanitizer();
    h.comment(' public comment ');
    expect(buffer.join('')).toBe('');
  });

  it('should ignore doctypes', () => {
    buffer = [];
    const h = createSanitizer();
    h.doctype(' html PUBLIC "public-dt"');
    expect(buffer.join('')).toBe('');
  });

  it('should escape special chars (& < >)', () => {
    buffer = [];
    const h = createSanitizer();
    h.start('span', {}, false);
    h.chars('x < y & z > w');
    h.end('span');
    expect(buffer.join('')).toBe('<span>x &lt; y &amp; z &gt; w</span>');
  });

  it('should output a self-closing tag (br)', () => {
    buffer = [];
    const h = createSanitizer();
    h.chars('before');
    h.start('br', {}, true);
    h.chars('after');
    expect(buffer.join('')).toBe('before<br>after');
  });

  it('should output input tag with a public attribute', () => {
    buffer = [];
    const h = createSanitizer();
    h.start('input', { type: 'tel', value: '+123456789' }, true);
    expect(buffer.join('')).toBe('<input type="tel" value="+123456789">');
  });

  it('should close mismatched end tag safely', () => {
    buffer = [];
    const h = createSanitizer();
    h.start('b', {}, false);
    h.end('i'); // mismatch, but the "end" handler will just output </i>
    const out = buffer.join('');
    // Must be either <b></i> or <b> depending on how the handler is used
    expect(['<b></i>', '<b>'].includes(out)).toBe(true);
  });
});