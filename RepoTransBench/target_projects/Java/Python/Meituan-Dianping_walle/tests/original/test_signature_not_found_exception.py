class SignatureNotFoundException(Exception):
    pass

def test_constructor_message():
    ex = SignatureNotFoundException("test message")
    assert str(ex) == "test message"
    assert ex.__cause__ is None

def test_constructor_message_and_cause():
    cause = RuntimeError("cause")
    try:
        raise SignatureNotFoundException("err") from cause
    except SignatureNotFoundException as ex:
        assert str(ex) == "err"
        assert ex.__cause__ == cause