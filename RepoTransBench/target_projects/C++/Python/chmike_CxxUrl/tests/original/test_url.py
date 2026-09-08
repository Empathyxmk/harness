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

# Test scheme normalization and validation
@pytest.mark.parametrize('input_scheme,expect_scheme,expect_error', [
    ('a', 'a', False),
    ('HTTP', 'http', False),
    ('HTTPs', 'https', False),
    ('X-1.0', 'x-1.0', False),
    ('X+a', 'x+a', False),
    ('', None, True),
    ('1A', None, True),
    ('a/5', None, True),
])
def test_scheme(input_scheme, expect_scheme, expect_error):
    if expect_error:
        with pytest.raises(UrlParseError):
            normalize_scheme(input_scheme)
    else:
        assert normalize_scheme(input_scheme) == expect_scheme


# Test user info parsing
@pytest.mark.parametrize('input_userinfo,expect_userinfo', [
    ('', ''),
    ('user:passwd', 'user:passwd'),
    ('user:pa%24%24wd', 'user:pa$$wd'),
])
def test_user_info(input_userinfo, expect_userinfo):
    assert normalize_user_info(input_userinfo) == expect_userinfo


def test_url_user_info_full():
    u = Url('http://user:pa%24%24wd@www.example.com')
    assert u.get_userinfo() == 'user:pa$$wd'


# Test host
@pytest.mark.parametrize('input_host,expected,expect_error', [
    ('', '', False),
    ('www.example.com', 'www.example.com', False),
    ('!$+', '!$+', False),
    ('12.34.56.78.com', '12.34.56.78.com', False),
    ('!#', None, True),
    ('12.34.56.78', '12.34.56.78', False),
    ('0.0.0.0', '0.0.0.0', False),
    ('12.34.56.257', None, True),
    # IPv6 cases handled in parametrize
])
def test_host(input_host, expected, expect_error):
    if expect_error:
        with pytest.raises(UrlParseError):
            normalize_host(input_host)
    else:
        assert normalize_host(input_host) == expected

# IPv6 hosts (normalized, mostly check for no error)
@pytest.mark.parametrize('input_host,expected,expect_error', [
    ('1:2:3:4:5:6:7:8', '1:2:3:4:5:6:7:8', False),
    ('1:2:3:4:5:6:9.9.9.9', '1:2:3:4:5:6:9.9.9.9', False),
    ('::9.9.9.9', '::9.9.9.9', False),
    ('::2:3:4:5:6:7:8', '0:2:3:4:5:6:7:8', False),  # Normalization may differ in real code
    ('::2:3:4:5:6:9.9.9.9', '0:2:3:4:5:6:9.9.9.9', False),
    ('1::4:5:6:7:8:9', '1:0:4:5:6:7:8:9', False),
    ('xxx', 'xxx', False),
    ('xxx::', None, True),
    ('x:x:x::x:x:x', None, True),
    ('x:x:x::x:x:x:y.y.y.y', None, True),
    ('1111:2222:3333:4444:5555:6666:7777:88889', None, True),
    ('1:2:3:4:5:6:7:8:9', None, True),
    (':1:2:3:4:5:6:7:8', None, True),
    (':1:2:3::6:7:8', None, True),
])
def test_host_ipv6(input_host, expected, expect_error):
    if expect_error:
        with pytest.raises(UrlParseError):
            normalize_host(input_host)
    else:
        assert normalize_host(input_host) == expected

# Test port
@pytest.mark.parametrize('input_port,expected,expect_error', [
    ('123', '123', False),
    ('0', '0', False),
    ('65535', '65535', False),
    ('65536', None, True),
    ('12a55', None, True),
])
def test_port(input_port, expected, expect_error):
    if expect_error:
        with pytest.raises(UrlParseError):
            normalize_port(input_port)
    else:
        assert normalize_port(input_port) == expected

# Test path normalization
@pytest.mark.parametrize('input_path,expected', [
    ('', ''),
    ('a', 'a'),
    ('.', ''),
    ('..', ''),
    ('a/', 'a/'),
    ('./', ''),
    ('../', ''),
    ('/a', '/a'),
    ('/.', '/'),
    ('/..', '/'),
    ('/a/', '/a/'),
    ('/./', '/'),
    ('/../', '/'),
    ('/a/', '/a/'),
    ('/a/a', '/a/a'),
    ('/./a', '/a'),
    ('/../a', '/a'),
    ('/a/.', '/a/'),
    ('/a/..', '/'),
    ('a/a', 'a/a'),
    ('./a', 'a'),
    ('../a', 'a'),
    ('a/.', 'a/'),
    ('a/..', ''),
    ('ab cd', 'ab cd'),
])
def test_path(input_path, expected):
    assert normalize_path(input_path) == expected

# Test fragment
@pytest.mark.parametrize('fragment,expected', [
    ('xxx', 'xxx'),
    ('ab cd', 'ab cd'),
])
def test_fragment(fragment, expected):
    assert normalize_fragment(fragment) == expected

# Test Url parsing and round trip
def test_url_str_empty():
    url = Url('')
    assert str(url) == ''
    assert url.get_path() == ''

def test_url_scheme_and_str():
    url = Url('http:')
    assert str(url) == 'http:'
    assert url.get_scheme() == 'http'
    url2 = Url('http:')
    assert str(url2) == 'http:'
    assert url2.get_scheme() == 'http'

def test_url_path_variations():
    u = Url('test/path')
    assert str(u) == 'test/path'
    assert u.get_path() == 'test/path'
    u = Url('test/path/..')
    assert u.get_path() == 'test'
    u = Url('test/path/../..')
    assert u.get_path() == ''
    u = Url('/test/path/../../')
    assert u.get_path() == '/'
    u = Url('/../..')
    assert u.get_path() == '/'

def test_url_percent_encoding():
    u1 = Url('test+path')
    assert str(u1) == 'test+path'
    u2 = Url('test%2bpath')
    assert str(u2) == 'test%2bpath'
    u3 = Url('test%20path')
    assert str(u3) == 'test%20path'
    u4 = Url('test%2Fpath')
    assert str(u4) == 'test%2Fpath'

def test_url_failures():
    with pytest.raises(UrlParseError):
        normalize_scheme('')
    with pytest.raises(UrlParseError):
        normalize_port('x')
    with pytest.raises(UrlParseError):
        normalize_host('12.34.56.257')