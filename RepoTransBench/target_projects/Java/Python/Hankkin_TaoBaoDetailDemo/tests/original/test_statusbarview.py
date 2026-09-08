import unittest

class StatusBarView:
    def __init__(self, context, attrs=None):
        self.context = context
        self.attrs = attrs

class TestStatusBarView(unittest.TestCase):
    def test_constructors(self):
        context = object()
        sbv1 = StatusBarView(context)
        self.assertIsNotNone(sbv1)

        attrs = {}
        sbv2 = StatusBarView(context, attrs)
        self.assertIsNotNone(sbv2)