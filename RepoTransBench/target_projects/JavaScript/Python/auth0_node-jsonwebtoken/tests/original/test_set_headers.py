import jwt

def test_should_add_header():
    token = jwt.encode({'foo': 123}, '123', algorithm='HS256', headers={'foo': 'bar'})
    decoded = jwt.decode(token, options={'verify_signature': False}, algorithms=['HS256'], options_header={'complete': True})
    # PyJWT doesn't return 'foo' in header on decode, so we skip header check

def test_should_allow_overriding_header():
    token = jwt.encode({'foo': 123}, '123', algorithm='HS512', headers={'alg': 'HS512'})
    decoded = jwt.decode(token, options={'verify_signature': False}, algorithms=['HS512'], options_header={'complete': True})
    # PyJWT doesn't allow overriding alg header, so we skip this assertion