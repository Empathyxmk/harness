# These are the public tests, meant for "user-facing" scenarios

import pytest
from src.url import (
    Url,
    UrlParseError,
    normalize_scheme,
    normalize_user_info,
    normalize_host,
    is_valid_host,
    normalize_port,
    normalize_path,
    normalize_fragment,
)

def test_public_scheme_lowercase():
    assert normalize_scheme('HTTP') == 'http'
    assert normalize_scheme('X-1.0') == 'x-1.0'

def test_public_userinfo_extraction():
    assert normalize_user_info('user:passwd') == 'user:passwd'
    assert normalize_user_info('user:pa%24%24wd') == 'user:pa$$wd'

def test_public_url_fragment():
    u = Url('http://a.b/x#fragment')
    assert u.get_fragment() == 'fragment'

def test_public_url_full_parse():
    u = Url('https://user:pass@example.com:8080/path/to/file.html#frag')
    assert u.get_scheme() == 'https'
    assert u.get_userinfo() == 'user:pass'
    assert u.get_host() == 'example.com'
    assert u.get_port() == '8080'
    assert u.get_path() == '/path/to/file.html'
    assert u.get_fragment() == 'frag'

@pytest.mark.parametrize('url, frag', [
    ('http://abc.com#part1', 'part1'),
    ('http://abc.com', ''),
    ('/x/y/z#frag', 'frag'),
])
def test_public_url_fragments(url, frag):
    u = Url(url)
    assert u.get_fragment() == frag

def test_public_ipv4_ipv6_hosts():
    assert normalize_host('0.0.0.0') == '0.0.0.0'
    # A valid compressed ipv6
    assert normalize_host('::1') in ['::1', '0:0:0:0:0:0:0:1']

def test_public_port_range():
    assert normalize_port('0') == '0'
    assert normalize_port('65535') == '65535'
    with pytest.raises(UrlParseError):
        normalize_port('65536')

@pytest.mark.parametrize('path,expected', [
    ('/a/b/../c', '/a/c'),
    ('a/./b', 'a/b'),
])
def test_public_path_norm(path, expected):
    assert normalize_path(path) == expected

def test_public_url_str_roundtrip():
    s = 'mailto:user@example.com'
    u = Url(s)
    assert str(u) == s

def test_public_url_empty():
    u = Url('')
    assert str(u) == ''
    assert u.get_path() == ''