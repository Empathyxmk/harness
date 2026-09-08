import pytest
from unittest import mock

class MultiTypeAdapter:
    class MultiViewTyper:
        def getViewType(self, obj):
            return 1  # Default implementation for testing

    def __init__(self, context):
        self.context = context
        self._viewtype_to_layout = {}
        self._items = []
        self._item_types = []

    def addViewTypeToLayoutMap(self, view_type, layout_res):
        self._viewtype_to_layout[view_type] = layout_res

    def add(self, obj, view_type=None):
        if view_type is None:
            raise ValueError("Must provide a view type")
        self._items.append(obj)
        self._item_types.append(view_type)

    def addAll(self, lst, view_type):
        for i in lst:
            self._items.append(i)
            self._item_types.append(view_type)

    def set(self, lst, typer_or_viewtype):
        self._items = []
        self._item_types = []
        if hasattr(typer_or_viewtype, 'getViewType'):
            for item in lst:
                self._items.append(item)
                self._item_types.append(typer_or_viewtype.getViewType(item))
        else:
            for item in lst:
                self._items.append(item)
                self._item_types.append(typer_or_viewtype)

    def getItemCount(self):
        return len(self._items)

    def getItemViewType(self, pos):
        return self._item_types[pos]

    def remove(self, idx):
        self._items.pop(idx)
        self._item_types.pop(idx)

    def clear(self):
        self._items = []
        self._item_types = []

    def addAllAtPosition(self, idx, lst, view_type):
        for offset, i in enumerate(lst):
            self._items.insert(idx + offset, i)
            self._item_types.insert(idx + offset, view_type)

    def addAtPosition(self, idx, item, view_type):
        self._items.insert(idx, item)
        self._item_types.insert(idx, view_type)

@pytest.fixture
def mock_context_and_inflater():
    context = mock.Mock()
    inflater = mock.Mock()
    context.getSystemService.return_value = inflater
    return context, inflater

def test_add_and_view_type(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    adapter = MultiTypeAdapter(context)
    adapter.addViewTypeToLayoutMap(1, 100)
    adapter.add("foo", 1)
    assert adapter.getItemCount() == 1
    assert adapter.getItemViewType(0) == 1

def test_add_all_and_set(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    adapter = MultiTypeAdapter(context)
    adapter.addViewTypeToLayoutMap(8, 108)
    lst = ["a", "b"]
    adapter.addAll(lst, 8)
    assert adapter.getItemCount() == 2
    assert adapter.getItemViewType(1) == 8
    adapter.set(["x", "y"], 8)
    assert adapter.getItemCount() == 2
    assert adapter.getItemViewType(0) == 8

def test_remove_clear(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    adapter = MultiTypeAdapter(context)
    adapter.addViewTypeToLayoutMap(2, 102)
    adapter.add("bar", 2)
    assert adapter.getItemCount() == 1
    adapter.remove(0)
    assert adapter.getItemCount() == 0
    adapter.add("foo", 2)
    adapter.clear()
    assert adapter.getItemCount() == 0

def test_set_with_typer(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    typer = mock.Mock()
    typer.getViewType.return_value = 3
    adapter = MultiTypeAdapter(context)
    adapter.addViewTypeToLayoutMap(3, 103)
    adapter.set(["f", "g"], typer)
    assert adapter.getItemCount() == 2
    assert adapter.getItemViewType(1) == 3

def test_add_at_position_and_add_all_position(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    adapter = MultiTypeAdapter(context)
    adapter.addViewTypeToLayoutMap(5, 105)
    adapter.add("m", 5)
    adapter.addAtPosition(0, "n", 5)
    lst = ["a", "b"]
    adapter.addAllAtPosition(0, lst, 5)
    assert adapter.getItemCount() == 4
    assert adapter.getItemViewType(2) == 5