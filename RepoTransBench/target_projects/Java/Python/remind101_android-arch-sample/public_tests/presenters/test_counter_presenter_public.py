import unittest

class Counter:
    def __init__(self, value=0):
        self.value = value

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value

class CounterPresenter:
    def __init__(self, counter):
        self.counter = counter
        self._view = None

    def attachView(self, view):
        self._view = view

    def isViewAttached(self):
        return self._view is not None

    def detachView(self):
        self._view = None

    def increment(self):
        self.counter.setValue(self.counter.getValue() + 1)
        if self._view:
            self._view.setValue(self.counter.getValue())
            self._view.showIncremented()

    def decrement(self):
        self.counter.setValue(self.counter.getValue() - 1)
        if self._view:
            self._view.setValue(self.counter.getValue())
            self._view.showDecremented()

class DummyView:
    def __init__(self):
        self.lastValue = -1
        self.onIncrement = False
        self.onDecrement = False

    def setValue(self, value):
        self.lastValue = value

    def showIncremented(self):
        self.onIncrement = True

    def showDecremented(self):
        self.onDecrement = True

class TestCounterPresenterPublic(unittest.TestCase):
    def setUp(self):
        self.counter = Counter(42)
        self.presenter = CounterPresenter(self.counter)

    def testIncrementPublic(self):
        view = DummyView()
        self.presenter.attachView(view)
        self.presenter.increment()
        self.assertEqual(43, self.counter.getValue())
        self.assertEqual(43, view.lastValue)
        self.assertTrue(view.onIncrement)

    def testDecrementPublic(self):
        view = DummyView()
        self.presenter.attachView(view)
        self.presenter.decrement()
        self.assertEqual(41, self.counter.getValue())
        self.assertEqual(41, view.lastValue)
        self.assertTrue(view.onDecrement)

    def testAttachDetachViewPublic(self):
        view = DummyView()
        self.presenter.attachView(view)
        self.assertTrue(self.presenter.isViewAttached())
        self.presenter.detachView()
        self.assertFalse(self.presenter.isViewAttached())

if __name__ == "__main__":
    unittest.main()