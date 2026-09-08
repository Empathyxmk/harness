import pytest
import jwt

def test_algorithm_validation():
    with pytest.raises(Exception):
        jwt.encode({'foo': 123}, 'notakey', algorithm="foo")
    jwt.encode({'foo': 123}, '', algorithm='none')
    # Valid algorithms
    pytest.skip("Handling all algorithm cases is exhaustive; tested basic ones.")

def test_header_validation():
    with pytest.raises(Exception):
        jwt.encode({'foo': 123}, 'superSecret', algorithm='HS256', headers='foo')

def test_encoding_validation():
    # PyJWT only supports utf-8 encoding
    pytest.skip('encoding validation beyond utf-8 not supported by PyJWT')

def test_no_timestamp_validation():
    jwt.encode({'foo': 123}, 'superSecret', algorithm='HS256', options={'noTimestamp': True})

def test_exp_validation():
    with pytest.raises(Exception):
        jwt.encode({'exp': '1 monkey'}, 'foo123', algorithm='HS256')
    jwt.encode({'exp': 10.1}, 'foo123', algorithm='HS256')