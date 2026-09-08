import pytest

class GridDataStructure:
    def __init__(self, lst, columns):
        self.lst = lst
        self.columns = columns

    def getRowCount(self):
        return (len(self.lst) + self.columns - 1) // self.columns

    def getDataForRow(self, rowIdx):
        begin = rowIdx * self.columns
        end = min(begin + self.columns, len(self.lst))
        if begin >= len(self.lst):
            raise IndexError("RowIdx out of range")
        return self.lst[begin:end]

@pytest.fixture
def grid_data():
    lst = ["A", "B", "C", "D", "E"]
    return GridDataStructure(lst, 2)

def test_get_row_count(grid_data):
    assert grid_data.getRowCount() == 3

def test_get_data_for_row(grid_data):
    row = grid_data.getDataForRow(1)
    assert row == ["C", "D"]

def test_get_data_for_last_row(grid_data):
    row = grid_data.getDataForRow(2)
    assert row == ["E"]

def test_get_data_for_row_invalid(grid_data):
    with pytest.raises(IndexError):
        grid_data.getDataForRow(6)