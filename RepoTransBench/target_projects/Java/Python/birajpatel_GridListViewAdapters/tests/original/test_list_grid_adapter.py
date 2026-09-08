import pytest

class ListGridAdapter:
    class RowPositionInfo:
        def __init__(self, rowIndex):
            self.rowIndex = rowIndex

    class RowViewHolder:
        def __init__(self):
            self.view = None
        def getView(self):
            return self.view

    def __init__(self, lst, columns):
        self.lst = lst
        self.columns = columns
        self.rowViewHolder = None

    def getCount(self):
        return (len(self.lst) + self.columns - 1) // self.columns

    def getItem(self, idx):
        if idx < 0 or idx >= self.getCount():
            raise IndexError("Index out of bounds")
        return self.lst

    def getRowPositionInfo(self, idx):
        return ListGridAdapter.RowPositionInfo(idx)

    def getView(self, idx, arg, parent):
        # Always returns a mocked view
        if self.rowViewHolder:
            return self.rowViewHolder.getView()
        return None

    def areAllItemsEnabled(self):
        return True

    def isEnabled(self, idx):
        return True

@pytest.fixture
def adapter():
    lst = ["A", "B", "C", "D", "E"]
    return ListGridAdapter(lst, 2)

def test_get_count(adapter):
    assert adapter.getCount() == 3

def test_get_item(adapter):
    assert adapter.getItem(0) == adapter.lst

def test_get_row_position_info(adapter):
    info = adapter.getRowPositionInfo(1)
    assert info.rowIndex == 1

def test_get_view_calls_row_view_holder(adapter, mocker):
    parent = mocker.Mock()
    holder = mocker.Mock()
    view = mocker.Mock()
    parent.getContext.return_value = None
    holder.getView.return_value = view

    # set private field rowViewHolder via monkey-patch
    adapter.rowViewHolder = holder
    result = adapter.getView(1, None, parent)
    assert result is not None

def test_are_all_items_enabled(adapter):
    assert adapter.areAllItemsEnabled()

def test_is_enabled(adapter):
    assert adapter.isEnabled(0)

def test_get_item_invalid_index(adapter):
    with pytest.raises(IndexError):
        adapter.getItem(10)