import pytest

class APIError(Exception):
    def __init__(self, message=None, code=None):
        super().__init__(message)
        self.name = 'APIError'
        self.message = message
        self.code = code
        self.status = 500

def test_apierror_sets_properties():
    err = APIError('something went wrong', 123)
    assert isinstance(err, Exception)
    assert getattr(err, 'name', None) == 'APIError'
    assert getattr(err, 'message', None) == 'something went wrong'
    assert getattr(err, 'code', None) == 123
    assert getattr(err, 'status', None) == 500
    assert isinstance(getattr(err, '__traceback__', None), type(err.__traceback__))

def test_apierror_message_and_code_can_be_none():
    err = APIError()
    assert getattr(err, 'message', None) is None
    assert getattr(err, 'code', None) is None