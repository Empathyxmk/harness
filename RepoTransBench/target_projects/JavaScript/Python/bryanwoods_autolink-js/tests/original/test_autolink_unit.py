import pytest
from src.autolink import autoLink

def test_returns_same_string_if_no_urls():
    assert autoLink('Hello there!') == 'Hello there!'

def test_links_a_simple_http_url():
    assert autoLink('Visit http://example.com.') == "Visit <a href='http://example.com'>http://example.com</a>."

def test_links_a_https_url_and_leaves_punctuation_outside_link():
    assert autoLink('Check this: https://example.com!') == "Check this: <a href='https://example.com'>https://example.com</a>!"

def test_links_an_ftp_url():
    assert autoLink('Files: ftp://ftp.example.com') == "Files: <a href='ftp://ftp.example.com'>ftp://ftp.example.com</a>"

def test_multiple_urls_in_string():
    assert autoLink('A: http://a.com B: http://b.com') == "A: <a href='http://a.com'>http://a.com</a> B: <a href='http://b.com'>http://b.com</a>"

def test_with_option_adds_attributes_to_link():
    result = autoLink('http://a.com', {'target': '_blank', 'rel': 'nofollow'})
    assert result == "<a href='http://a.com' target='_blank' rel='nofollow'>http://a.com</a>"

def test_with_option_calls_callback_and_uses_its_return_value():
    cb = lambda url: f"<x-link>{url}</x-link>"
    result = autoLink('Start http://ex.com here', {'callback': cb})
    assert result == 'Start <x-link>http://ex.com</x-link> here'

def test_with_option_callback_returns_falsy_should_fallback_to_link():
    # Python: None is falsy, so falls back to link
    result = autoLink('Find http://ex.com', {'callback': None, 'class': 'foo'})
    assert result == "Find <a href='http://ex.com' class='foo'>http://ex.com</a>"

def test_pattern_matching_ignores_html_tags():
    assert autoLink('<b>http://site.com</b>') == "<b><a href='http://site.com'>http://site.com</a></b>"

def test_edge_empty_string_returns_empty_string():
    assert autoLink('') == ''

def test_url_at_beginning_of_string():
    assert autoLink('http://start.com is a start.') == "<a href='http://start.com'>http://start.com</a> is a start."

def test_url_with_hash_and_percent_chars():
    assert autoLink('see http://foo.com/#section?val=100%25') == \
        "see <a href='http://foo.com/#section?val=100%25'>http://foo.com/#section?val=100%25</a>"

def test_no_options_argument():
    assert autoLink('foo http://bar.com') == "foo <a href='http://bar.com'>http://bar.com</a>"