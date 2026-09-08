import unittest

class StatusBarView:
    def __init__(self, context, attrs=None):
        self.context = context
        self.attrs = attrs

class TestStatusBarViewPublic(unittest.TestCase):
    class DummyContext:
        pass

    def test_constructor_with_context(self):
        ctx = self.DummyContext()
        sbv = StatusBarView(ctx)
        self.assertIsNotNone(sbv)

    def test_constructor_with_context_and_attrs(self):
        ctx = self.DummyContext()
        attrs = None
        sbv = StatusBarView(ctx, attrs)
        self.assertIsNotNone(sbv)