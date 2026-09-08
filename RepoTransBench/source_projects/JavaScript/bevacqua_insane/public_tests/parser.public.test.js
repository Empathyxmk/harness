const parser = require('../parser');

describe('parser (public)', () => {
  it('should parse simple single tag', () => {
    const html = '<h1>Hello</h1>';
    const events = [];
    parser(html, {
      start: (tag, attrs, unary) => events.push(`start:${tag}`),
      end: tag => events.push(`end:${tag}`),
      chars: text => events.push(`text:${text}`),
      comment: text => events.push(`comment:${text}`),
    });
    expect(events).toEqual(['start:h1', 'text:Hello', 'end:h1']);
  });

  it('should parse nested tags and text', () => {
    const html = '<div><span>Nice!</span>Text</div>';
    const out = [];
    parser(html, {
      start: (tag, attrs, unary) => out.push(`<${tag}>`),
      end: tag => out.push(`</${tag}>`),
      chars: text => out.push(text),
    });
    expect(out).toEqual(['<div>', '<span>', 'Nice!', '</span>', 'Text', '</div>']);
  });

  it('should trigger comment callback for HTML comments', () => {
    const html = '<div><!--something--></div>';
    const events = [];
    parser(html, {
      start: (tag, attrs, unary) => events.push(`S:${tag}`),
      end: tag => events.push(`E:${tag}`),
      chars: () => {},
      comment: text => events.push(`C:${text}`),
    });
    // don't check value of comment, just check comment triggered
    expect(events).toEqual(['S:div', 'C:something', 'E:div']);
  });
});