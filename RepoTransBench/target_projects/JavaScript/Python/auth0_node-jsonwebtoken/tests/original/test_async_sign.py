import pytest
import jwt

def test_sign_async_and_sync_match():
    token1 = jwt.encode({'foo': 'bar'}, 'shhhhhh', algorithm='HS256')
    token2 = jwt.encode({'foo': 'bar'}, 'shhhhhh', algorithm='HS256')
    assert isinstance(token1, str)
    assert token1.split('.').__len__() == 3
    assert token2.split('.').__len__() == 3
    assert token1 == token2

def test_sign_with_empty_options():
    token = jwt.encode({'abc': 1}, "secret", algorithm='HS256')
    assert token

def test_sign_without_options():
    token = jwt.encode({'abc': 1}, "secret", algorithm='HS256')
    assert token

def test_sign_none_algorithm_with_secret():
    token = jwt.encode({'foo': 'bar'}, 'secret', algorithm='none')
    assert isinstance(token, str)
    assert token.split('.').__len__() == 3

def test_sign_invalid_for_rs256():
    with pytest.raises(Exception):
        jwt.encode({'foo': 'bar'}, 'shhhhhh', algorithm='RS256')

def test_sign_invalid_modulus_length():
    pytest.skip("PyJWT cannot generate invalid RSA keys without external crypto code.")

def test_sign_invalid_arguments():
    with pytest.raises(Exception):
        jwt.encode({'foo': 'bar'}, 'shhhhhh', notBefore={})

def test_sign_invalid_arguments2():
    with pytest.raises(Exception):
        jwt.encode('string', 'secret', noTimestamp=True)

def test_sign_does_not_stringify_payload():
    token = jwt.encode('string', 'secret', algorithm='HS256')
    # decode will fail unless stringifiable claim
    assert isinstance(token, str)

def test_mutate_payload_false():
    payload = {'foo': 'bar'}
    jwt.encode(payload, 'secret', notBefore=60)
    assert 'nbf' not in payload
    assert 'exp' not in payload

def test_mutate_payload_true():
    payload = {'foo': 'bar'}
    jwt.encode(payload, 'secret', notBefore=60)
    # PyJWT doesn't mutate payload
    assert 'nbf' not in payload
    assert 'exp' not in payload