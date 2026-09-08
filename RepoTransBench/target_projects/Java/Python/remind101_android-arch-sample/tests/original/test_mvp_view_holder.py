import unittest

class DummyBasePresenter:
    def __init__(self):
        self.wasBind = False
    def bindView(self, view):
        self.wasBind = True

class DummyViewHolder:
    def __init__(self, itemView):
        self.itemView = itemView
        self.presenter = None

    def bindPresenter(self, presenter):
        self.presenter = presenter
        presenter.bindView(self)

    def unbindPresenter(self):
        self.presenter = None

class TestMvpViewHolder(unittest.TestCase):
    def testBindAndUnbindPresenter(self):
        presenter = DummyBasePresenter()
        itemView = object()
        vh = DummyViewHolder(itemView)
        vh.bindPresenter(presenter)
        self.assertEqual(presenter, vh.presenter)
        self.assertTrue(presenter.wasBind)
        vh.unbindPresenter()
        self.assertIsNone(vh.presenter)

if __name__ == "__main__":
    unittest.main()