import jwt

def test_sign_string():
    token = jwt.encode('hello', '123', algorithm='HS256')
    decoded = jwt.decode(token, '123', algorithms=['HS256'])
    assert decoded == 'hello'

def test_sign_number():
    token = jwt.encode(123, '123', algorithm='HS256')
    decoded = jwt.decode(token, '123', algorithms=['HS256'])
    assert decoded == '123'