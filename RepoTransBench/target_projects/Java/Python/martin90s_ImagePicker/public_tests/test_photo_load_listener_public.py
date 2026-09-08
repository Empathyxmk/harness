import pytest

class PhotoLoadListener:
    def on_photo_loaded(self, count):
        raise NotImplementedError

class DummyListener(PhotoLoadListener):
    def __init__(self):
        self.last_count = -2
        self.called = False
    def on_photo_loaded(self, count):
        self.last_count = count
        self.called = True

def test_photo_load_listener_with_different_count():
    listener = DummyListener()
    listener.on_photo_loaded(7)
    assert listener.called
    assert listener.last_count == 7

def test_photo_load_listener_multiple_calls():
    listener = DummyListener()
    listener.on_photo_loaded(2)
    assert listener.called
    assert listener.last_count == 2
    listener.on_photo_loaded(12)
    assert listener.last_count == 12