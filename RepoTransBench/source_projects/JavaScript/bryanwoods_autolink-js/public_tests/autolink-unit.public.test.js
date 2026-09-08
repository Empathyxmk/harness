const path = require('path');
require(path.resolve(__dirname, '../autolink.js'));

describe('autoLink (public cases)', () => {
  test('returns the same string if there are no URLs (different string)', () => {
    expect('No links here!'.autoLink()).toBe('No links here!');
  });

  test('links a simple https URL (different domain)', () => {
    expect('Visit https://mysite.org.'.autoLink()).toBe("Visit <a href='https://mysite.org'>https://mysite.org</a>.");
  });

  test('links a ftp URL and leaves punctuation outside the link (different domain, punctuation)', () => {
    expect('Here: ftp://downloads.test.net.'.autoLink()).toBe("Here: <a href='ftp://downloads.test.net'>ftp://downloads.test.net</a>.");
  });

  test('links an http URL (different domain)', () => {
    expect('Website: http://abc.xyz'.autoLink()).toBe("Website: <a href='http://abc.xyz'>http://abc.xyz</a>");
  });

  test('multiple URLs in a string (different domains)', () => {
    expect('X: https://x.org Y: https://y.org'.autoLink()).toBe("X: <a href='https://x.org'>https://x.org</a> Y: <a href='https://y.org'>https://y.org</a>");
  });

  test('with option: adds data attributes to link (different attr)', () => {
    expect('https://mysite.org'.autoLink({target: '_self', 'data-extra': '42'}))
      .toBe("<a href='https://mysite.org' target='_self' data-extra='42'>https://mysite.org</a>");
  });

  test('with option: calls callback and uses its return value (different wrapper)', () => {
    const cb = (url) => `<span class="url">${url}</span>`;
    expect('Link: ftp://content.com'.autoLink({ callback: cb }))
      .toBe('Link: <span class="url">ftp://content.com</span>');
  });

  test('with option: callback returns undefined, uses link with custom class (different)', () => {
    expect('Details at https://about.org'.autoLink({ callback: undefined, class: 'custom' }))
      .toBe("Details at <a href='https://about.org' class='custom'>https://about.org</a>");
  });

  test('pattern matching: ignores HTML tags (different tag and protocol)', () => {
    expect('<i>ftp://tagged.site</i>'.autoLink())
      .toBe("<i><a href='ftp://tagged.site'>ftp://tagged.site</a></i>");
  });

  test('edge: whitespace string returns whitespace string', () => {
    expect('   '.autoLink()).toBe('   ');
  });

  test('URL at end of string', () => {
    expect('Ends at https://finish.net.'.autoLink())
      .toBe("Ends at <a href='https://finish.net'>https://finish.net</a>.");
  });

  test('URL with ? and & chars', () => {
    expect('Go: https://foo.org/page?param1=a&param2=b'.autoLink())
      .toBe("Go: <a href='https://foo.org/page?param1=a&param2=b'>https://foo.org/page?param1=a&param2=b</a>");
  });

  test('no options argument (different domain)', () => {
    expect('baz https://baz.net'.autoLink()).toBe("baz <a href='https://baz.net'>https://baz.net</a>");
  });
});