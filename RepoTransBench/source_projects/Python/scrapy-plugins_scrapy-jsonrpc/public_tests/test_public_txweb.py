import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrapy_jsonrpc.txweb import Error, Handler, NOT_FOUND

def test_public_error_properties():
    err = Error(1000, "unknown error", data={"prop": "value"})
    assert err.code == 1000
    assert err.message == "unknown error"
    assert err.data == {"prop": "value"}

def test_public_error_str_repr():
    err = Error(404, "resource not here")
    assert str(err) == "resource not here"
    assert repr(err) == "Error(404, 'resource not here')"

def test_public_handler_returns_not_found():
    class DummyHandler(Handler):
        def __call__(self, *args, **kwargs):
            raise NOT_FOUND
    handler = DummyHandler()
    try:
        handler()
    except Exception as e:
        assert isinstance(e, Error)
        assert e.code == 404
        assert e.message == "Not Found"