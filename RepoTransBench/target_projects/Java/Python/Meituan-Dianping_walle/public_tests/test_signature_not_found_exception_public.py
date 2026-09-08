class SignatureNotFoundException(Exception):
    pass

def test_constructor_message_public():
    ex = SignatureNotFoundException("another message")
    assert str(ex) == "another message"
    assert ex.__cause__ is None

def test_constructor_message_and_cause_public():
    cause = Exception("public cause")
    try:
        raise SignatureNotFoundException("public error") from cause
    except SignatureNotFoundException as ex:
        assert str(ex) == "public error"
        assert ex.__cause__ == cause