import pytest

class PhotoLoadListener:
    def on_load_complete(self, photo_uris):
        raise NotImplementedError
    def on_load_error(self):
        raise NotImplementedError

class DummyListener(PhotoLoadListener):
    def __init__(self):
        self.on_load_complete_called = False
        self.on_load_error_called = False

    def on_load_complete(self, photo_uris):
        self.on_load_complete_called = True
        assert photo_uris is not None

    def on_load_error(self):
        self.on_load_error_called = True

def test_listener():
    listener = DummyListener()
    listener.on_load_complete([])
    listener.on_load_error()
    assert listener.on_load_complete_called
    assert listener.on_load_error_called