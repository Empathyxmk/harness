import pytest
from unittest import mock

class BindingViewHolder:
    pass

class BaseViewAdapter:
    class Decorator:
        pass

    class Presenter:
        pass

    def __init__(self, context):
        self.context = context
        self.mCollection = []
        self._presenter = None
        self.mDecorator = None

    def add(self, item):
        self.mCollection.append(item)

    def set(self, items):
        self.mCollection = list(items)

    def clear(self):
        self.mCollection = []

    def getItemCount(self):
        return len(self.mCollection)

    def remove(self, idx):
        self.mCollection.pop(idx)

    def get(self, idx):
        return self.mCollection[idx]

    def setPresenter(self, p):
        self._presenter = p

    def getPresenter(self):
        return self._presenter

    def setDecorator(self, d):
        self.mDecorator = d

class TestAdapter(BaseViewAdapter):
    def __init__(self, context):
        super().__init__(context)

@pytest.fixture
def mock_context_and_inflater():
    context = mock.Mock()
    inflater = mock.Mock()
    context.getSystemService.return_value = inflater
    return context, inflater

def test_add_set_clear_public(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    adapter = TestAdapter(context)
    adapter.add("red")
    assert adapter.getItemCount() == 1
    adapter.set(["yellow", "green", "blue"])
    assert adapter.getItemCount() == 3
    adapter.clear()
    assert adapter.getItemCount() == 0

def test_remove_get_public(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    adapter = TestAdapter(context)
    adapter.set(["x", "y", "z"])
    assert adapter.get(1) == "y"
    adapter.remove(0)
    assert adapter.get(0) == "y"
    assert adapter.getItemCount() == 2