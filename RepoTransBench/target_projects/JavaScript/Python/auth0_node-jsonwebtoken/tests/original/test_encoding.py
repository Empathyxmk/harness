import pytest
import jwt
import base64

def test_properly_encodes_token_utf8():
    expected = 'José'
    token = jwt.encode({'name': expected}, 'shhhhh', algorithm='HS256')
    parts = token.split('.')
    import base64
    decoded_name = jwt.decode(token, 'shhhhh', algorithms=['HS256'])['name']
    assert decoded_name == expected

def test_properly_encodes_token_binary():
    pytest.skip("Binary encoding not supported by PyJWT.")

def test_decodes_unicode():
    username = "測試"
    token = jwt.encode({"username": username}, "test", algorithm="HS256")
    payload = jwt.decode(token, "test", algorithms=["HS256"])
    assert payload["username"] == username