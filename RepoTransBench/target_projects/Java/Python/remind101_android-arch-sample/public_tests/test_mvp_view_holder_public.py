import unittest

class DummyPresenter:
    pass

class DummyViewHolder:
    def __init__(self):
        self.bindCalled = False
        self.unbindCalled = False
        self.boundPresenter = None

    def bindPresenter(self, presenter):
        self.bindCalled = True
        self.boundPresenter = presenter

    def unbindPresenter(self):
        self.unbindCalled = True
        self.boundPresenter = None

class TestMvpViewHolderPublic(unittest.TestCase):
    def testBindAndUnbindPresenterPublic(self):
        presenter = DummyPresenter()
        viewHolder = DummyViewHolder()
        viewHolder.bindPresenter(presenter)
        self.assertTrue(viewHolder.bindCalled)
        self.assertEqual(presenter, viewHolder.boundPresenter)
        viewHolder.unbindPresenter()
        self.assertTrue(viewHolder.unbindCalled)
        self.assertIsNone(viewHolder.boundPresenter)

if __name__ == "__main__":
    unittest.main()