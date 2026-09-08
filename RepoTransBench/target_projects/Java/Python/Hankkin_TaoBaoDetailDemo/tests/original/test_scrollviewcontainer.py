import unittest

class ScrollViewContainer:
    def __init__(self, context, attrs=None, defStyle=0):
        self.context = context
        self.attrs = attrs
        self.defStyle = defStyle

class TestScrollViewContainer(unittest.TestCase):

    def setUp(self):
        self.context = object() # Dummy context

    def test_constructors_and_init(self):
        sc1 = ScrollViewContainer(self.context)
        self.assertIsNotNone(sc1)
        attrs = None
        sc2 = ScrollViewContainer(self.context, attrs)
        self.assertIsNotNone(sc2)
        sc3 = ScrollViewContainer(self.context, attrs, 0)
        self.assertIsNotNone(sc3)