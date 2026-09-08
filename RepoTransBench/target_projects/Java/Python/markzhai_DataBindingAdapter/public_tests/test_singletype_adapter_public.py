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

def test_add_and_count_public(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    adapter = SingleTypeAdapter(context, 1222)
    adapter.add("delta")
    assert adapter.getItemCount() == 1
    assert adapter.getLayoutRes() == 1222

def test_add_at_position_public(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    adapter = SingleTypeAdapter(context, 2121)
    adapter.add("sigma")
    adapter.addAtPosition(0, "theta")
    assert adapter.getItemCount() == 2
    assert adapter.mCollection[0] == "theta"
    assert adapter.mCollection[1] == "sigma"

def test_set_public(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    adapter = SingleTypeAdapter(context, 3333)
    items = ["alpha", "beta", "gamma"]
    adapter.set(items)
    assert adapter.getItemCount() == 3
    assert adapter.mCollection[0] == "alpha"
    assert adapter.mCollection[2] == "gamma"

def test_add_all_public(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    adapter = SingleTypeAdapter(context, 4343)
    items = ["one", "two"]
    adapter.addAll(items)
    assert adapter.getItemCount() == 2
    adapter.add("three")
    assert adapter.getItemCount() == 3