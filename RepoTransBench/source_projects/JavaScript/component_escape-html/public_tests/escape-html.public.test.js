const escapeHtml = require('../index');

describe('escapeHtml - public tests', () => {
  it('should return the same string if there are no escapable characters', () => {
    expect(escapeHtml('Public abc123 test')).toBe('Public abc123 test');
  });

  it('should escape a double quote (")', () => {
    expect(escapeHtml('She said: "Hello!"')).toBe('She said: &quot;Hello!&quot;');
  });

  it('should escape a single quote (\')', () => {
    expect(escapeHtml("It\'s a public test")).toBe('It&#39;s a public test');
  });

  it('should escape an ampersand (&)', () => {
    expect(escapeHtml('Fish & Chips')).toBe('Fish &amp; Chips');
  });

  it('should escape a less-than-sign (<)', () => {
    expect(escapeHtml('<section>')).toBe('&lt;section&gt;');
  });

  it('should handle multiple types of escapable characters', () => {
    expect(escapeHtml('5 > 2 && 2 < 4 "quoted" \'single\''))
      .toBe('5 &gt; 2 &amp;&amp; 2 &lt; 4 &quot;quoted&quot; &#39;single&#39;');
  });

  it('should escape already escaped HTML characters again', () => {
    expect(escapeHtml('&quot; &gt; &#39;'))
      .toBe('&amp;quot; &amp;gt; &amp;#39;');
  });

  it('should work with string inputs that are Numbers', () => {
    expect(escapeHtml(2024)).toBe('2024');
  });

  it('should work with empty string', () => {
    expect(escapeHtml('')).toBe('');
  });

  it('should not escape characters outside ["\'&<>]', () => {
    expect(escapeHtml('!@$%^()[]=+')).toBe('!@$%^()[]=+');
  });
});