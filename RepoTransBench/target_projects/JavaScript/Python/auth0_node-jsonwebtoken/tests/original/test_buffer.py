import jwt

def test_buffer_payload():
    import base64
    payload = base64.b64decode('TkJyotZe8NFpgdfnmgINqg==')
    token = jwt.encode(payload.decode(), "signing key", algorithm='HS256')
    assert jwt.decode(token, "signing key", algorithms=['HS256']) == payload.decode()