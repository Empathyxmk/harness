def test_invalidjsonexception_message_public():
    class InvalidJsonException(Exception):
        def __init__(self, message):
            super().__init__(message)
    e = InvalidJsonException("New message for public test")
    assert str(e) == "New message for public test"

def test_invalidjsonexception_null_message_public():
    class InvalidJsonException(Exception):
        def __init__(self, message):
            super().__init__(message)
    e = InvalidJsonException(None)
    assert e.args[0] is None