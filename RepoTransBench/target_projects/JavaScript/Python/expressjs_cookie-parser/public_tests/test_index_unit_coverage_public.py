import pytest
from src.cookie_parser import signedCookies, cookieParser

def object_with_null_proto(d=None):
    class NullProtoDict(dict):
        pass
    obj = NullProtoDict()
    if d:
        for k, v in d.items():
            obj[k] = v
    return obj

def test_should_decode_signed_cookies_and_remove_from_original_object_public_data():
    obj = object_with_null_proto({'d': 'xyz', 'c': 's:data.nope'})
    secrets = ['secret squirrel']
    decoded = signedCookies(obj, secrets)
    expected = object_with_null_proto({'c': False})
    assert type(decoded) == type(expected)
    assert dict(decoded) == dict(expected)

def test_should_return_empty_object_if_no_signed_values_different_data():
    obj = object_with_null_proto({'e': 'plain'})
    secrets = ['another secret']
    result = signedCookies(obj, secrets)
    expected = object_with_null_proto()
    assert type(result) == type(expected)
    assert dict(result) == dict(expected)

def test_cookie_parser_middleware_edge_cases_public_should_handle_no_cookies_case_different_req_headers():
    req = type('Req', (), {})()
    req.headers = {}
    res = object()
    called = {}
    def next_func():
        assert type(req.cookies) == type(object_with_null_proto())
        assert dict(req.cookies) == {}
        called['ok'] = True
    mw = cookieParser()
    mw(req, res, next_func)
    assert called.get('ok', False)