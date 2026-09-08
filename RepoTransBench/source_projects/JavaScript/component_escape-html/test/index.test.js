const escapeHtml = require('../index');

describe('escapeHtml', () => {
  it('should return the same string if no escapable characters', () => {
    expect(escapeHtml('foo bar baz')).toBe('foo bar baz');
  });

  it('should escape double quotes', () => {
    expect(escapeHtml('he said "hi"')).toBe('he said &quot;hi&quot;');
  });

  it("should escape single quotes", () => {
    expect(escapeHtml("it's ok")).toBe('it&#39;s ok');
  });

  it('should escape ampersands', () => {
    expect(escapeHtml('AT&T')).toBe('AT&amp;T');
  });

  it('should escape less than symbol', () => {
    expect(escapeHtml('1 < 2')).toBe('1 &lt; 2');
  });

  it('should escape greater than symbol', () => {
    expect(escapeHtml('2 > 1')).toBe('2 &gt; 1');
  });

  it('should handle multiple escapable characters', () => {
    expect(escapeHtml('rock & roll > pop < classical "music" ain\'t bad')).toBe(
      'rock &amp; roll &gt; pop &lt; classical &quot;music&quot; ain&#39;t bad'
    );
  });

  it('should not double escape', () => {
    expect(escapeHtml('&quot;')).toBe('&amp;quot;');
  });

  it('should work with numeric string', () => {
    expect(escapeHtml('12345')).toBe('12345');
  });

  it('should return empty string for empty input', () => {
    expect(escapeHtml('')).toBe('');
  });
});