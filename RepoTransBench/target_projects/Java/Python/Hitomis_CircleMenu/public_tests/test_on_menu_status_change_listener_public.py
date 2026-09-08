import unittest

class OnMenuStatusChangeListener:
    def onMenuOpened(self):
        raise NotImplementedError()
    def onMenuClosed(self):
        raise NotImplementedError()

class TestOnMenuStatusChangeListenerPublic(unittest.TestCase):
    def test_onMenuOpened_and_onMenuClosed_different(self):
        class TestListener(OnMenuStatusChangeListener):
            def onMenuOpened(self):
                status = "OpenedPublic"
                assert status == "OpenedPublic"
            def onMenuClosed(self):
                status = "ClosedPublic"
                assert status == "ClosedPublic"
        listener = TestListener()
        listener.onMenuOpened()
        listener.onMenuClosed()