const path = require('path');
require(path.resolve(__dirname, '../autolink.js'));

describe('autoLink', () => {
  test('returns the same string if there are no URLs', () => {
    expect('Hello there!'.autoLink()).toBe('Hello there!');
  });

  test('links a simple http URL', () => {
    expect('Visit http://example.com.'.autoLink()).toBe("Visit <a href='http://example.com'>http://example.com</a>.");
  });

  test('links a https URL and leaves punctuation outside the link', () => {
    expect('Check this: https://example.com!'.autoLink()).toBe("Check this: <a href='https://example.com'>https://example.com</a>!");
  });

  test('links an ftp URL', () => {
    expect('Files: ftp://ftp.example.com'.autoLink()).toBe("Files: <a href='ftp://ftp.example.com'>ftp://ftp.example.com</a>");
  });

  test('multiple URLs in a string', () => {
    expect('A: http://a.com B: http://b.com'.autoLink()).toBe("A: <a href='http://a.com'>http://a.com</a> B: <a href='http://b.com'>http://b.com</a>");
  });

  test('with option: adds attributes to link', () => {
    expect('http://a.com'.autoLink({target: '_blank', rel: 'nofollow'}))
      .toBe("<a href='http://a.com' target='_blank' rel='nofollow'>http://a.com</a>");
  });

  test('with option: calls callback and uses its return value', () => {
    const cb = (url) => `<x-link>${url}</x-link>`;
    expect('Start http://ex.com here'.autoLink({ callback: cb }))
      .toBe('Start <x-link>http://ex.com</x-link> here');
  });

  test('with option: callback returns falsy, should fall back to link', () => {
    expect('Find http://ex.com'.autoLink({ callback: null, class: 'foo' }))
      .toBe("Find <a href='http://ex.com' class='foo'>http://ex.com</a>");
  });

  test('pattern matching: ignores HTML tags', () => {
    expect('<b>http://site.com</b>'.autoLink()).toBe("<b><a href='http://site.com'>http://site.com</a></b>");
    // Preceded by a tag will still match (per regex)
  });

  test('edge: empty string returns empty string', () => {
    expect(''.autoLink()).toBe('');
  });

  test('URL at beginning of string', () => {
    expect('http://start.com is a start.'.autoLink()).toBe("<a href='http://start.com'>http://start.com</a> is a start.");
  });

  test('URL with # and % chars', () => {
    expect('see http://foo.com/#section?val=100%25'.autoLink())
      .toBe("see <a href='http://foo.com/#section?val=100%25'>http://foo.com/#section?val=100%25</a>");
  });

  test('no options argument', () => {
    expect('foo http://bar.com'.autoLink()).toBe("foo <a href='http://bar.com'>http://bar.com</a>");
  });
});