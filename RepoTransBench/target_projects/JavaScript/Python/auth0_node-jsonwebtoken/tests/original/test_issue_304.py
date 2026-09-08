import jwt
import pytest

def test_verify_number_should_fail():
    with pytest.raises(jwt.InvalidTokenError):
        jwt.decode(123, 'foo', algorithms=["HS256"])

def test_verify_object_should_fail():
    with pytest.raises(jwt.InvalidTokenError):
        jwt.decode({'foo': 'bar'}, 'biz', algorithms=["HS256"])

def test_verify_array_should_fail():
    with pytest.raises(jwt.InvalidTokenError):
        jwt.decode(['foo'], 'bar', algorithms=["HS256"])

def test_verify_function_should_fail():
    with pytest.raises(jwt.InvalidTokenError):
        jwt.decode(lambda: None, 'foo', algorithms=["HS256"])

def test_verify_boolean_should_fail():
    with pytest.raises(jwt.InvalidTokenError):
        jwt.decode(True, 'foo', algorithms=["HS256"])