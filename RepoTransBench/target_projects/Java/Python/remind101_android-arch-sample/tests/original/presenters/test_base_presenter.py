import unittest

class BasePresenter:
    def __init__(self):
        self._view = None

    def bindView(self, view):
        self._view = view

    def getView(self):
        return self._view

    def unbindView(self):
        self._view = None

class DummyView:
    pass

class DummyPresenter(BasePresenter):
    pass

class TestBasePresenter(unittest.TestCase):
    def testBindViewAndUnbindView(self):
        presenter = DummyPresenter()
        view = DummyView()
        presenter.bindView(view)
        self.assertIsNotNone(presenter.getView())
        presenter.unbindView()
        self.assertIsNone(presenter.getView())

if __name__ == "__main__":
    unittest.main()