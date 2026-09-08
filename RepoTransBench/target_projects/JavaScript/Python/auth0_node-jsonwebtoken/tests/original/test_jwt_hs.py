import pytest
import jwt

def test_sign_hs256_secret_is_asym():
    pytest.skip("Checking for symmetric key is not supported directly by PyJWT.")

def test_sign_payload_undefined():
    with pytest.raises(TypeError):
        jwt.encode(None, "secret", algorithm='HS256')

def test_sign_options_not_plain_object():
    pytest.skip("Options as list is not supported in PyJWT and is a type error in Python.")

def test_hs256_token_is_valid():
    secret = "shhhhhh"
    token = jwt.encode({'foo': 'bar'}, secret, algorithm='HS256')
    assert isinstance(token, str)
    assert token.split('.').__len__() == 3
    verified = jwt.decode(token, secret, algorithms=['HS256'])
    assert verified['foo'] == 'bar'

def test_validate_with_secret():
    secret = "shhhhhh"
    token = jwt.encode({'foo': 'bar'}, secret, algorithm='HS256')
    verified = jwt.decode(token, secret, algorithms=['HS256'])
    assert verified['foo'] == 'bar'

def test_throw_with_invalid_secret():
    secret = "shhhhhh"
    token = jwt.encode({'foo': 'bar'}, secret, algorithm='HS256')
    with pytest.raises(jwt.exceptions.InvalidSignatureError):
        jwt.decode(token, 'invalid secret', algorithms=['HS256'])

def test_throw_with_null():
    with pytest.raises(Exception):
        jwt.decode(None, 'secret', algorithms=['HS256'])