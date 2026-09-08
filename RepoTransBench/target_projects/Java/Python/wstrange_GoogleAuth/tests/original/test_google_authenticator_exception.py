def test_exception_message():
    ex = Exception("A message")
    assert str(ex) == "A message"

def test_exception_cause():
    class CustomException(Exception):
        def __init__(self, msg, cause):
            super().__init__(msg)
            self.__cause__ = cause

    cause = RuntimeError("root")
    ex = CustomException("A message", cause)
    assert str(ex) == "A message"
    assert ex.__cause__ == cause