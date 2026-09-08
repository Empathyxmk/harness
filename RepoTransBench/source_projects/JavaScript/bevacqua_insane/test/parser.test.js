const parser = require('../parser');

describe('parser', () => {
  it('should parse and handle tags and chars', () => {
    const events = [];
    parser('<div class="a">hi<b>bye</b><!--comment--></div>', {
      start: (tag, attrs, unary) => events.push(['start', tag, attrs, unary]),
      end: (tag) => events.push(['end', tag]),
      chars: (text) => events.push(['chars', text]),
      comment: (c) => events.push(['comment', c]),
    });
    expect(events).toEqual([
      ['start', 'div', { class: 'a' }, false],
      ['chars', 'hi'],
      ['start', 'b', {}, false],
      ['chars', 'bye'],
      ['end', 'b'],
      ['comment', 'comment'],
      ['end', 'div'],
    ]);
  });

  it('should handle unary tags', () => {
    const events = [];
    parser('<img src="x"/>', {
      start: (tag, attrs, unary) => events.push([tag, unary, attrs]),
      end: (tag) => events.push(['end', tag]),
    });
    expect(events[0][0]).toBe('img');
    expect(events[0][1]).toBe(true);
    expect(events[0][2].src).toBe('x');
  });

  it('should handle tags with no attributes', () => {
    const events = [];
    parser('<div></div>', {
      start: (t, a, u) => events.push(['start', t, a, u]),
      end: (t) => events.push(['end', t]),
    });
    expect(events.length).toBeGreaterThan(1);
  });

  it('should decode attribute values', () => {
    let atts = null;
    parser('<a href="&lt;">', {
      start: (t, a, u) => { atts = a; },
      end: () => {},
    });
    expect(atts.href).toBe('<');
  });

  it('should handle unquoted attributes', () => {
    let atts = null;
    parser('<a href=foo>', {
      start: (t, a, u) => { atts = a; },
      end: () => {},
    });
    expect(atts.href).toBe('foo');
  });

  it('should handle boolean attribute', () => {
    let atts = null;
    parser('<button disabled>', {
      start: (t, a, u) => { atts = a; },
      end: () => {},
    });
    expect(atts.disabled).toBeUndefined();
  });
});