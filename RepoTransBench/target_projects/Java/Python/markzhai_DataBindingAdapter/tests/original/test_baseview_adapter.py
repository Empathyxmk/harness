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

    def remove(self, idx):
        self.mCollection.pop(idx)

    def getItemCount(self):
        return len(self.mCollection)

    def clear(self):
        self.mCollection = []

    def setPresenter(self, p):
        self._presenter = p

    def getPresenter(self):
        return self._presenter

    def setDecorator(self, d):
        self.mDecorator = d

    def get(self, idx):
        return self.mCollection[idx]

class TestAdapter(BaseViewAdapter):
    def __init__(self, c):
        super().__init__(c)
        self.mCollection = []

@pytest.fixture
def setup_adapter():
    context = mock.Mock()
    inflater = mock.Mock()
    context.getSystemService.return_value = inflater
    adapter = TestAdapter(context)
    adapter.mCollection.extend(["a", "b", "c"])
    return adapter

def test_remove(setup_adapter):
    adapter = setup_adapter
    adapter.remove(1)
    assert adapter.getItemCount() == 2
    assert adapter.mCollection[0] == "a"
    assert adapter.mCollection[1] == "c"

def test_clear(setup_adapter):
    adapter = setup_adapter
    adapter.clear()
    assert adapter.getItemCount() == 0

def test_set_presenter_and_decorator(setup_adapter):
    adapter = setup_adapter
    p = mock.Mock(spec=BaseViewAdapter.Presenter)
    adapter.setPresenter(p)
    assert adapter.getPresenter() == p

    d = mock.Mock(spec=BaseViewAdapter.Decorator)
    adapter.setDecorator(d)
    assert adapter.mDecorator is not None