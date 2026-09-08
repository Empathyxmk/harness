import pytest
from src.autolink import autoLink

def test_returns_same_string_if_no_urls_different_string():
    assert autoLink('No links here!') == 'No links here!'

def test_links_a_simple_https_url_different_domain():
    assert autoLink('Visit https://mysite.org.') == "Visit <a href='https://mysite.org'>https://mysite.org</a>."

def test_links_a_ftp_url_and_leaves_punctuation_outside_link_different_domain_punctuation():
    assert autoLink('Here: ftp://downloads.test.net.') == "Here: <a href='ftp://downloads.test.net'>ftp://downloads.test.net</a>."

def test_links_an_http_url_different_domain():
    assert autoLink('Website: http://abc.xyz') == "Website: <a href='http://abc.xyz'>http://abc.xyz</a>"

def test_multiple_urls_in_a_string_different_domains():
    assert autoLink('X: https://x.org Y: https://y.org') == \
           "X: <a href='https://x.org'>https://x.org</a> Y: <a href='https://y.org'>https://y.org</a>"

def test_with_option_adds_data_attributes_to_link_different_attr():
    result = autoLink('https://mysite.org', {'target': '_self', 'data-extra': '42'})
    assert result == "<a href='https://mysite.org' target='_self' data-extra='42'>https://mysite.org</a>"

def test_with_option_calls_callback_and_uses_its_return_value_different_wrapper():
    cb = lambda url: f'<span class="url">{url}</span>'
    result = autoLink('Link: ftp://content.com', {'callback': cb})
    assert result == 'Link: <span class="url">ftp://content.com</span>'

def test_with_option_callback_returns_undefined_uses_link_with_custom_class_different():
    # In JS, undefined is falsy; in Python, None is the default for not passed; use None to simulate JS undefined.
    result = autoLink('Details at https://about.org', {'callback': None, 'class': 'custom'})
    assert result == "Details at <a href='https://about.org' class='custom'>https://about.org</a>"

def test_pattern_matching_ignores_html_tags_different_tag_and_protocol():
    assert autoLink('<i>ftp://tagged.site</i>') == "<i><a href='ftp://tagged.site'>ftp://tagged.site</a></i>"

def test_edge_whitespace_string_returns_whitespace_string():
    assert autoLink('   ') == '   '

def test_url_at_end_of_string():
    assert autoLink('Ends at https://finish.net.') == \
        "Ends at <a href='https://finish.net'>https://finish.net</a>."

def test_url_with_question_and_and_chars():
    assert autoLink('Go: https://foo.org/page?param1=a&param2=b') == \
        "Go: <a href='https://foo.org/page?param1=a&param2=b'>https://foo.org/page?param1=a&param2=b</a>"

def test_no_options_argument_different_domain():
    assert autoLink('baz https://baz.net') == "baz <a href='https://baz.net'>https://baz.net</a>"