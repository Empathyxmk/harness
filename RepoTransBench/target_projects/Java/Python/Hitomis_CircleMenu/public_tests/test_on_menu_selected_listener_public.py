import unittest

class OnMenuSelectedListener:
    def onMenuSelected(self, index):
        raise NotImplementedError()

class TestOnMenuSelectedListenerPublic(unittest.TestCase):
    def test_onMenuSelected_withDifferentIndex(self):
        class TestListener(OnMenuSelectedListener):
            def onMenuSelected(self, index):
                assert index == 2
        listener = TestListener()
        listener.onMenuSelected(2)