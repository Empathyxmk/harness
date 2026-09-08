import pytest
from unittest import mock

class MultiTypeAdapter:
    class MultiViewTyper:
        def getViewType(self, obj):
            return 1  # Default

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

def test_add_and_view_type_public(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    adapter = MultiTypeAdapter(context)
    adapter.addViewTypeToLayoutMap(9, 109)
    adapter.add("baz", 9)
    assert adapter.getItemCount() == 1
    assert adapter.getItemViewType(0) == 9

def test_add_all_and_set_public(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    adapter = MultiTypeAdapter(context)
    adapter.addViewTypeToLayoutMap(11, 111)
    lst = ["p", "q", "r"]
    adapter.addAll(lst, 11)
    assert adapter.getItemCount() == 3
    assert adapter.getItemViewType(2) == 11
    adapter.set(["v", "w", "z"], 11)
    assert adapter.getItemCount() == 3
    assert adapter.getItemViewType(0) == 11

def test_remove_clear_public(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    adapter = MultiTypeAdapter(context)
    adapter.addViewTypeToLayoutMap(7, 107)
    adapter.add("car", 7)
    assert adapter.getItemCount() == 1
    adapter.remove(0)
    assert adapter.getItemCount() == 0
    adapter.add("bus", 7)
    adapter.clear()
    assert adapter.getItemCount() == 0

def test_set_with_typer_public(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    typer = mock.Mock()
    typer.getViewType.return_value = 4
    adapter = MultiTypeAdapter(context)
    adapter.addViewTypeToLayoutMap(4, 104)
    adapter.set(["k", "l", "m"], typer)
    assert adapter.getItemCount() == 3
    assert adapter.getItemViewType(2) == 4

def test_add_at_position_and_add_all_position_public(mock_context_and_inflater):
    context, _ = mock_context_and_inflater
    adapter = MultiTypeAdapter(context)
    adapter.addViewTypeToLayoutMap(15, 115)
    adapter.add("apple", 15)
    adapter.addAtPosition(0, "banana", 15)
    lst = ["pear", "peach"]
    adapter.addAllAtPosition(0, lst, 15)
    assert adapter.getItemCount() == 4
    assert adapter.getItemViewType(3) == 15