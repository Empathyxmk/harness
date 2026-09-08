from src.cookie_parser import cookieParser
import pytest

def normalize(obj):
    if obj is None or not isinstance(obj, dict):
        return obj
    return dict(obj)

def test_signedCookies_should_decode_signed_cookies_and_remove_from_original_changed_data():
    from src.cookie_parser import signedCookies
    result = signedCookies({'bar': 's:12345.signature'}, 'baz')
    assert normalize(result) == normalize({'bar': False})

def test_signedCookies_should_return_empty_object_if_no_signed_cookies_changed_data():
    from src.cookie_parser import signedCookies
    result = signedCookies({'foo': 'plain'}, 'baz')
    assert normalize(result) == normalize({})

def test_signedCookies_should_work_with_empty_input_public_variant():
    from src.cookie_parser import signedCookies
    result = signedCookies({}, 'quux')
    assert normalize(result) == normalize({})

def test_cookieParser_internal_should_populate_req_cookies_and_signedCookies_for_empty_cookies_public():
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