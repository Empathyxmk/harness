import pytest
import jwt

def test_fail_with_string():
    broken_token = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
                    'eyJleHAiOiIxMjMiLCJmb28iOiJhZGFzIn0.'
                    'cDa81le-pnwJMcJi3o3PBwB7cTJMiXCkizIhxbXAKRg')
    with pytest.raises(jwt.exceptions.InvalidTokenError):
        jwt.decode(broken_token, '123', algorithms=['HS256'])

def test_fail_with_0():
    broken_token = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
                    'eyJleHAiOjAsImZvbyI6ImFkYXMifQ.'
                    'UKxix5T79WwfqAA0fLZr6UrhU-jMES2unwCOFa4grEA')
    with pytest.raises(jwt.exceptions.ExpiredSignatureError):
        jwt.decode(broken_token, '123', algorithms=['HS256'])

def test_fail_with_false():
    broken_token = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
                    'eyJleHAiOmZhbHNlLCJmb28iOiJhZGFzIn0.'
                    'iBn33Plwhp-ZFXqppCd8YtED77dwWU0h68QS_nEQL8I')
    with pytest.raises(jwt.exceptions.InvalidTokenError):
        jwt.decode(broken_token, '123', algorithms=['HS256'])

def test_fail_with_true():
    broken_token = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
                    'eyJleHAiOnRydWUsImZvbyI6ImFkYXMifQ.'
                    'eOWfZCTM5CNYHAKSdFzzk2tDkPQmRT17yqllO-ItIMM')
    with pytest.raises(jwt.exceptions.InvalidTokenError):
        jwt.decode(broken_token, '123', algorithms=['HS256'])

def test_fail_with_object():
    broken_token = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
                    'eyJleHAiOnt9LCJmb28iOiJhZGFzIn0.'
                    '1JjCTsWLJ2DF-CfESjLdLfKutUt3Ji9cC7ESlcoBHSY')
    with pytest.raises(jwt.exceptions.InvalidTokenError):
        jwt.decode(broken_token, '123', algorithms=['HS256'])