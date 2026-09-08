const insane = require('../insane');

describe('insane', () => {
  it('should export defaults', () => {
    expect(insane.defaults).toBeTruthy();
  });

  it('should sanitize html with defaults', () => {
    const result = insane('<div onclick="evil()">hello <a href="javascript:evil()">link</a></div>');
    expect(result).toContain('<div>');
    expect(result).toContain('hello');
    // Should not include the onclick attr or javascript url
    expect(result).not.toContain('onclick');
    expect(result).toContain('<a>');
  });

  it('should allow allowed options', () => {
    const result = insane('<a href="http://safe">ok</a>', {
      allowedTags: ['a'], allowedAttributes: { a: ['href'] }, allowedSchemes: ['http'],
    }, true);
    expect(result).toContain('href="http://safe"');
    expect(result).toContain('<a');
  });

  it('should work with strict mode', () => {
    // strict === true should use passed options
    const result = insane('<span class="asdf">xx</span>', {
      allowedTags: ['span'],
      allowedAttributes: { span: ['class'] },
      allowedClasses: { span: ['asdf'] },
    }, true);
    expect(result).toContain('class="asdf"');
  });

  it('should fallback to defaults if strict !== true', () => {
    const result = insane('<hr noshade>', { allowedTags: ['hr'], allowedAttributes: { hr: ['noshade'] } });
    expect(result).toContain('<hr');
  });
});