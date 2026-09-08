import pytest
import jwt
import time

def test_no_timestamp_with_string():
    token = jwt.encode({'foo': 123}, '123', expires_delta=300, options={'noTimestamp': True})
    decoded = jwt.decode(token, '123', algorithms=['HS256'])
    assert abs(decoded['exp'] - (int(time.time()) + (5*60))) <= 1  # Allow small tolerance