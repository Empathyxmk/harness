import unittest

class OnMenuSelectedListener:
    def onMenuSelected(self, index):
        raise NotImplementedError()

class TestListener(OnMenuSelectedListener):
    def __init__(self):
        self.lastSelectedIndex = -1

    def onMenuSelected(self, index):
        self.lastSelectedIndex = index

class TestOnMenuSelectedListener(unittest.TestCase):
    def test_OnMenuSelectedCalled(self):
        listener = TestListener()
        listener.onMenuSelected(2)
        self.assertEqual(2, listener.lastSelectedIndex)
        listener.onMenuSelected(0)
        self.assertEqual(0, listener.lastSelectedIndex)