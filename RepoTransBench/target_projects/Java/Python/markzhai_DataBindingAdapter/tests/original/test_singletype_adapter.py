import pytest
from unittest import mock

class SingleTypeAdapter:
    def __init__(self, context, layout_res):
        self.context = context
        self.layout_res = layout_res
        self.mCollection = []

    def getItemCount(self):
        return len(self.mCollection)

    def add(self, value):
        self.mCollection.append(value)

    def addAtPosition(self, idx, value):
        self.mCollection.insert(idx, value)

    def addAll(self, lst):
        self.mCollection.extend(lst)

    def set(self, lst):
        self.mCollection = list(lst)

    def getLayoutRes(self):
        return self.layout_res

@pytest.fixture
def mock_context_and_inflater():
    context = mock.Mock()
    inflater = mock.Mock()
    context.getSystemService.return_value = inflater
    return context, inflater

def test_constructor_and_getters(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    adapter = SingleTypeAdapter(context, 123)
    assert adapter.getItemCount() == 0
    assert adapter.getLayoutRes() == 123

def test_add(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    adapter = SingleTypeAdapter(context, 321)
    adapter.add("foo")
    assert adapter.getItemCount() == 1

def test_add_at_position(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    adapter = SingleTypeAdapter(context, 321)
    adapter.add("foo")
    adapter.addAtPosition(0, "bar")
    assert adapter.getItemCount() == 2

def test_set_and_add_all(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    adapter = SingleTypeAdapter(context, 321)
    adapter.set(["a", "b"])
    assert adapter.getItemCount() == 2
    adapter.addAll(["c"])
    assert adapter.getItemCount() == 3