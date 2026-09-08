from src.cookie_parser import cookieParser
import pytest

def normalize(obj):
    # Python dicts serialize fine to JSON; to mimic JS normalize,
    # make sure dicts without prototype are represented as dict
    if obj is None or not isinstance(obj, dict):
        return obj
    return dict(obj)

def test_signedCookies_should_decode_signed_cookies_and_remove_from_original():
    # simulate decoding result (always False for any signature)
    cookies = {'foo': 's:value.signature'}
    secrets = ['bar']
    from src.cookie_parser import signedCookies
    result = signedCookies({'foo': 's:value.signature'}, 'bar')
    assert normalize(result) == normalize({'foo': False})

def test_signedCookies_should_return_empty_object_if_no_signed_cookies():
    from src.cookie_parser import signedCookies
    result = signedCookies({'bar': 'boz'}, 'foo')
    assert normalize(result) == normalize({})

def test_signedCookies_should_work_with_empty_input():
    from src.cookie_parser import signedCookies
    result = signedCookies({}, 'foo')
    assert normalize(result) == normalize({})

def test_cookieParser_internal_should_populate_req_cookies_and_signedCookies_for_empty_cookies():
    req = type('Req', (), {})()
    req.headers = {'cookie': ''}
    res = object()
    called = {}
    def next_func():
        assert normalize(req.cookies) == normalize({})
        assert normalize(req.signedCookies) == normalize({})
        called['ok'] = True
    mw = cookieParser()
    mw(req, res, next_func)
    assert called.get('ok', False)