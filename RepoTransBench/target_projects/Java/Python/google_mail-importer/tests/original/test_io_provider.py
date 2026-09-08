import pytest


class DummyIoProvider:
    def __init__(self, throw_exception):
        self.throw_exception = throw_exception

    def get(self):
        if self.throw_exception:
            raise IOError("fail")
        return "success"


def test_get_success():
    io_provider = DummyIoProvider(False)
    assert io_provider.get() == "success"


def test_get_throws_ioerror():
    io_provider = DummyIoProvider(True)
    with pytest.raises(IOError) as excinfo:
        io_provider.get()
    assert str(excinfo.value) == "fail"