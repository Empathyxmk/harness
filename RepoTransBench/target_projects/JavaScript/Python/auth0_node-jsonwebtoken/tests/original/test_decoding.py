import jwt

def test_should_not_crash_on_decoding_null():
    # In JS, decoding "null" string returns null; in PyJWT, returns None
    decoded = jwt.decode("null", options={"verify_signature": False})
    assert decoded is None