import pytest
import jsonlines

def test_readerwriterbase_repr():
    from jsonlines.jsonlines import ReaderWriterBase

    class Dummy(ReaderWriterBase):
        def __init__(self):
            self._closed = False  # Needed by parent
        def _repr_for_wrapped(self):
            return "<wrapped>"

    dummy = Dummy()
    result = repr(dummy)
    assert "<wrapped>" in result

def test_readerwriterbase_close_closes_fp(monkeypatch):
    from jsonlines.jsonlines import ReaderWriterBase

    class DummyFP:
        def __init__(self):
            self.closed = False
        def close(self):
            self.closed = True

    class Dummy(ReaderWriterBase):
        def __init__(self):
            self._fp = DummyFP()
            self._should_close_fp = True
            self._closed = False
        def _repr_for_wrapped(self):
            return "<wrapped>"

    dummy = Dummy()
    dummy.close()
    assert dummy._fp.closed
    assert dummy._closed

def test_default_dumps_notimplemented():
    from jsonlines.jsonlines import default_dumps
    with pytest.raises(NotImplementedError):
        default_dumps("abc")