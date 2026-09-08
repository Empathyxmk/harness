import unittest
from unittest.mock import MagicMock, call

class Counter:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.value = 0

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value

class CounterPresenter:
    def __init__(self):
        self._view = None
        self._model = None

    def bindView(self, view):
        self._view = view

    def getView(self):
        return self._view

    def setModel(self, model):
        self._model = model
        self.updateView()

    def updateView(self):
        view = self.getView()
        counter = self._model
        if view and counter:
            view.setCounterName(counter.getName())
            view.setCounterValue(counter.getValue())
            view.setMinusButtonEnabled(counter.getValue() > 0)
            view.setPlusButtonEnabled(counter.getValue() < 99)

    def onMinusButtonClicked(self):
        if self._model.getValue() > 0:
            self._model.setValue(self._model.getValue() - 1)

    def onPlusButtonClicked(self):
        if self._model.getValue() < 99:
            self._model.setValue(self._model.getValue() + 1)

    def onCounterClicked(self):
        view = self.getView()
        if view:
            view.goToDetailView(self._model)

class TestCounterPresenter(unittest.TestCase):
    def setUp(self):
        self.presenter = CounterPresenter()
        self.view = MagicMock()
        self.presenter.bindView(self.view)
        self.counter = Counter()
        self.counter.setId(4)
        self.counter.setName("My Counter")
        self.counter.setValue(18)

    def testUpdateView_setsName(self):
        self.presenter.setModel(self.counter)
        self.view.setCounterName.assert_called_with("My Counter")

    def testUpdateView_setsValue(self):
        self.presenter.setModel(self.counter)
        self.view.setCounterValue.assert_called_with(18)

    def testUpdateView_whenCounterGreaterThan0_setsMinusButtonEnabled(self):
        self.presenter.setModel(self.counter)
        self.view.setMinusButtonEnabled.assert_called_with(True)

    def testUpdateView_whenCounterEqual0_setsMinusButtonDisabled(self):
        self.counter.setValue(0)
        self.presenter.setModel(self.counter)
        self.view.setMinusButtonEnabled.assert_called_with(False)

    def testUpdateView_whenCounterLowerThan99_setsPlusButtonEnabled(self):
        self.presenter.setModel(self.counter)
        self.view.setPlusButtonEnabled.assert_called_with(True)

    def testUpdateView_whenCounterEqual99_setsMinusButtonDisabled(self):
        self.counter.setValue(99)
        self.presenter.setModel(self.counter)
        self.view.setPlusButtonEnabled.assert_called_with(False)

    def testOnMinusButtonClicked_whenCounterGreaterThan0_decrementsValue(self):
        self.counter.setValue(16)
        self.presenter.setModel(self.counter)
        self.view.reset_mock()
        self.presenter.onMinusButtonClicked()
        self.assertEqual(self.counter.getValue(), 15)

    def testOnMinusButtonClicked_whenCounterEquals0_doesNotDoAnything(self):
        self.counter.setValue(0)
        self.presenter.setModel(self.counter)
        self.view.reset_mock()
        self.presenter.onMinusButtonClicked()
        self.assertEqual(self.counter.getValue(), 0)

    def testOnPlusButtonClicked_whenCounterLowerThan99_incrementsValue(self):
        self.counter.setValue(16)
        self.presenter.setModel(self.counter)
        self.view.reset_mock()
        self.presenter.onPlusButtonClicked()
        self.assertEqual(self.counter.getValue(), 17)

    def testOnPlusButtonClicked_whenCounterEquals99_doesNotDoAnything(self):
        self.counter.setValue(99)
        self.presenter.setModel(self.counter)
        self.view.reset_mock()
        self.presenter.onPlusButtonClicked()
        self.assertEqual(self.counter.getValue(), 99)

    def testOnCounterClicked_opensDetailView(self):
        self.presenter.setModel(self.counter)
        self.view.reset_mock()
        self.presenter.onCounterClicked()
        self.view.goToDetailView.assert_called_with(self.counter)

if __name__ == "__main__":
    unittest.main()