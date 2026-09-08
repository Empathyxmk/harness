import pytest
from threading import Event

class DiscoverListener:
    def changed(self, changed_path):
        pass

def test_discover_with_different_path():
    path = "/public/test/path"
    called = [False]

    class MyListener(DiscoverListener):
        def changed(self, changed_path):
            if changed_path == path:
                called[0] = True

    listener = MyListener()
    listener.changed(path)
    assert called[0], "Listener should be called with public path"