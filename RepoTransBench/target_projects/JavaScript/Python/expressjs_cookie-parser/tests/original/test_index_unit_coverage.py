import pytest
from src.cookie_parser import signedCookies, cookieParser

def object_with_null_proto(d=None):
    """Simulates JS Object.create(null)"""
    class NullProtoDict(dict):
        pass
    obj = NullProtoDict()
    if d:
        for k, v in d.items():
            obj[k] = v
    return obj

def test_should_decode_signed_cookies_and_remove_from_original_object_fixed_for_null_prototype():
    # Arrange: 'b' is signed (invalid), 'a' is plain.
    obj = object_with_null_proto({'a': 'val', 'b': 's:val.signature'})
    secrets = ['keyboard cat']
    decoded = signedCookies(obj, secrets)
    assert type(decoded).__name__ != 'dict'
    # Should be { b: False } with null-proto
    expected = object_with_null_proto({'b': False})
    assert dict(decoded) == dict(expected)
    assert type(decoded) == type(expected)

def test_should_return_empty_object_if_no_signed_values_fixed_for_null_prototype():
    obj = object_with_null_proto({'a': 'val'})
    secrets = ['keyboard cat']
    result = signedCookies(obj, secrets)
    assert type(result).__name__ != 'dict'
    expected = object_with_null_proto()
    assert dict(result) == dict(expected)
    assert type(result) == type(expected)

def test_cookie_parser_middleware_edge_cases_should_handle_no_cookies_case_fixed_for_null_prototype():
    req = type('Req', (), {})()
    req.headers = {}
    res = object()
    called = {}

    def next_func():
        called['ok'] = True
        assert type(req.cookies).__name__ != 'dict'
        assert dict(req.cookies) == {}
        assert type(req.cookies) == type(object_with_null_proto())

    mw = cookieParser()
    mw(req, res, next_func)
    assert called.get('ok', False)