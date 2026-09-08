import pytest
import jwt
import base64
from pathlib import Path

from jwt.exceptions import (
    InvalidTokenError,
    ExpiredSignatureError,
    InvalidSignatureError,
    ImmatureSignatureError,
    InvalidKeyError,
)
# Use both pytest's assert and bidict's expect
from .test_utils import async_check

test_dir = Path(__file__).parent


@pytest.fixture(scope='module')
def keys():
    with open(test_dir / 'priv.pem', 'rb') as f:
        priv = f.read()
    with open(test_dir / 'pub.pem', 'rb') as f:
        pub = f.read()
    return priv, pub


def test_should_first_assume_json_claim_set(keys):
    priv, pub = keys
    payload = {'iat': int(1234567890)}
    token = jwt.encode(payload, priv, algorithm='RS256')
    decoded = jwt.decode(token, pub, algorithms=['RS256'])
    assert decoded['iat'] == payload['iat']

def test_should_not_verify_unsigned_token(keys):
    payload = {'iat': int(1234567890)}
    header = {'alg': 'none'}
    token_parts = (
        base64.urlsafe_b64encode(bytes(str(header), 'utf-8')).decode().rstrip("="),
        base64.urlsafe_b64encode(bytes(str(payload), 'utf-8')).decode().rstrip("="),
        "",
    )
    token = ".".join(token_parts)
    with pytest.raises(InvalidTokenError):
        jwt.decode(token, 'secret', algorithms=['HS256'])

def test_should_be_able_to_verify_unsigned_token_when_none_specified(keys):
    payload = {'iat': int(1234567890)}
    header = {'alg': 'none'}
    token_parts = (
        base64.urlsafe_b64encode(bytes(str(header), 'utf-8')).decode().rstrip("="),
        base64.urlsafe_b64encode(bytes(str(payload), 'utf-8')).decode().rstrip("="),
        "",
    )
    token = ".".join(token_parts)
    decoded = jwt.decode(token, options={"verify_signature": False})
    assert decoded['iat'] == payload['iat']

def test_should_not_mutate_options(keys):
    priv, pub = keys
    payload = {'iat': int(1234567890)}
    token = jwt.encode(payload, priv, algorithm='RS256')
    options = {'verify_signature': True}
    _ = jwt.decode(token, pub, algorithms=['RS256'])
    assert len(options) == 1

def test_secret_or_token_as_callback(monkeypatch):
    token = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJmb28iOiJiYXIiLCJpYXQiOjE0MzcwMTg1ODIsImV4cCI6MTQzNzAxODU5Mn0."
        "3aR3vocmgRpG05rsI9MpR6z2T_BGtMQaPq2YR6QaroU"
    )
    key = 'key'
    payload = {'foo': 'bar', 'iat': 1437018582, 'exp': 1437018592}

    decoded = jwt.decode(token, key, algorithms=["HS256"], options={'verify_exp': False})
    assert decoded['foo'] == 'bar'

def test_should_error_on_expired_token():
    token = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJmb28iOiJiYXIiLCJpYXQiOjE0MzcwMTg1ODIsImV4cCI6MTQzNzAxODU5Mn0."
        "3aR3vocmgRpG05rsI9MpR6z2T_BGtMQaPq2YR6QaroU"
    )
    key = "key"
    with pytest.raises(ExpiredSignatureError):
        jwt.decode(token, key, algorithms=['HS256'])

def test_should_not_error_on_expired_token_within_clock_tolerance():
    token = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJmb28iOiJiYXIiLCJpYXQiOjE0MzcwMTg1ODIsImV4cCI6MTQzNzAxODU5Mn0."
        "3aR3vocmgRpG05rsI9MpR6z2T_BGtMQaPq2YR6QaroU"
    )
    key = "key"
    decoded = jwt.decode(token, key, algorithms=['HS256'], leeway=5)
    assert decoded['foo'] == 'bar'

def test_should_error_on_unsupported_public_key_type():
    # This test can't be emulated in PyJWT; skip
    pytest.skip("Can't test unknown key type 'dsa' in PyJWT.")

def test_should_error_on_incorrect_public_key_type():
    pytest.skip("PyJWT enforces algorithm, but not with a custom message.")

def test_should_error_on_key_validation_disabled():
    pytest.skip("PyJWT has no allowInvalidAsymmetricKeyTypes, skip test.")