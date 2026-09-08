def test_invalidjsonexception_constructor_with_message_and_throwable():
    class InvalidJsonException(Exception):
        def __init__(self, message, cause=None):
            super().__init__(message)
            self.cause = cause
        def getMessage(self):
            return str(self)
        def getCause(self):
            return self.cause
    t = RuntimeError("test")
    ex = InvalidJsonException("message", t)
    assert "message" in str(ex)
    assert ex.getCause() is t