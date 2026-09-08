import pytest
import jwt

def test_expires_in_seconds_deprecated():
    with pytest.raises(TypeError):
        jwt.encode({'foo': 123}, '123', expiresInSeconds=5)