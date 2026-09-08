import pytest
import jwt

TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.t-IDcSemACt8x4iTMCda8Yhe3iZaWbvV5XKSTbuAn0M'

def test_verify_null():
    with pytest.raises(jwt.InvalidTokenError):
        jwt.decode(TOKEN, None, algorithms=["HS256"])

def test_verify_undefined():
    with pytest.raises(TypeError):
        jwt.decode(TOKEN, algorithms=["HS256"])