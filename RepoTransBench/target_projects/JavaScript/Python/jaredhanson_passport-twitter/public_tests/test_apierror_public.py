import pytest

class APIError(Exception):
    def __init__(self, message=None, code=None):
        super().__init__(message)
        self.name = 'APIError'
        self.message = message
        self.code = code
        self.status = 500

def test_apierror_public_set_properties():
    err = APIError('another error occurred', 999)
    assert isinstance(err, Exception)
    assert getattr(err, 'name', None) == 'APIError'
    assert getattr(err, 'message', None) == 'another error occurred'
    assert getattr(err, 'code', None) == 999
    assert getattr(err, 'status', None) == 500
    assert isinstance(getattr(err, '__traceback__', None), type(err.__traceback__))

def test_apierror_public_missing_values():
    err = APIError(None, None)
    assert getattr(err, 'message', None) is None
    assert getattr(err, 'code', None) is None