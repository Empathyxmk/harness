import unittest

class OnMenuStatusChangeListener:
    def onMenuOpened(self):
        raise NotImplementedError()
    def onMenuClosed(self):
        raise NotImplementedError()

class TestListener(OnMenuStatusChangeListener):
    def __init__(self):
        self.opened = False
        self.closed = False

    def onMenuOpened(self):
        self.opened = True

    def onMenuClosed(self):
        self.closed = True

class TestOnMenuStatusChangeListener(unittest.TestCase):
    def test_OnMenuOpenedAndClosed(self):
        listener = TestListener()
        self.assertFalse(listener.opened)
        self.assertFalse(listener.closed)

        listener.onMenuOpened()
        self.assertTrue(listener.opened)

        listener.onMenuClosed()
        self.assertTrue(listener.closed)