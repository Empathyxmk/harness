import unittest

class BasePresenter:
    def __init__(self):
        self._view = None

    def attachView(self, view):
        self._view = view

    def isViewAttached(self):
        return self._view is not None

    def getView(self):
        return self._view

    def detachView(self):
        self._view = None

class DummyPresenter(BasePresenter):
    pass

class TestBasePresenterPublic(unittest.TestCase):
    def testBasePresenterAttachAndDetachViewPublic(self):
        presenter = DummyPresenter()
        view = "PUBLIC_TEST_VIEW"
        presenter.attachView(view)
        self.assertTrue(presenter.isViewAttached())
        self.assertEqual(view, presenter.getView())
        presenter.detachView()
        self.assertFalse(presenter.isViewAttached())
        self.assertIsNone(presenter.getView())

if __name__ == "__main__":
    unittest.main()