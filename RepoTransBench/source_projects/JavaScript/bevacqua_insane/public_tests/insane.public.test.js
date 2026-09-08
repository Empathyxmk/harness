const insane = require('../insane');

describe('insane (public)', () => {
  it('should export defaults object', () => {
    expect(typeof insane.defaults).toBe('object');
    expect(insane.defaults).not.toBeNull();
  });

  it('should sanitize html with defaults and strip unsafe content', () => {
    const result = insane('<p style="color:red">Safe <script>bad()</script>text <img src="javascript:bad()" /></p>');
    expect(result).toContain('<p');
    expect(result).toContain('Safe');
    expect(result).not.toContain('script');
    expect(result).not.toContain('javascript:bad()');
    expect(result).toContain('<img');
  });

  it('should allow safe URLs with custom allowed options', () => {
    const result = insane('<img src="https://safeimage.com/x.png">', {
      allowedTags: ['img'],
      allowedAttributes: { img: ['src'] }, allowedSchemes: ['https'],
    }, true);
    expect(result).toContain('src="https://safeimage.com/x.png"');
    expect(result).toContain('<img');
  });

  it('should work with different strict true config', () => {
    const html = '<section class="main">abc</section>';
    const result = insane(html, {
      allowedTags: ['section'],
      allowedAttributes: { section: ['class'] },
      allowedClasses: { section: ['main'] },
    }, true);
    expect(result).toContain('class="main"');
    expect(result).toContain('section');
  });

  it('should return fallback to defaults if strict not true', () => {
    const html = '<br nobr>';
    const result = insane(html, { allowedTags: ['br'], allowedAttributes: { br: ['nobr'] } });
    expect(result).toContain('<br');
  });
});