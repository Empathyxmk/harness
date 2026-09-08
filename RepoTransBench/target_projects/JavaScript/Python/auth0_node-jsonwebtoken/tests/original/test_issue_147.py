import jwt
import pytest
import time

def test_sign_object_seal_sets_exp():
    # Python has no Object.seal, so regular dict
    token = jwt.encode({'foo': 123}, '123', algorithm='HS256', expires_delta=10)
    res = jwt.decode(token, '123', algorithms=['HS256'])
    # Allow a 1s tolerance due to execution time
    assert abs(res['exp'] - (int(time.time()) + 10)) <= 1