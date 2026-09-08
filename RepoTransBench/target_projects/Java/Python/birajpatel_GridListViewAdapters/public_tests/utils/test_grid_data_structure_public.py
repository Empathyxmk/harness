def test_get_set_item_public():
    class GridDataStructure:
        def __init__(self, rows, cols):
            self.rows = rows
            self.cols = cols
            self._data = [[None for _ in range(cols)] for _ in range(rows)]
        def setItem(self, r, c, val):
            self._data[r][c] = val
        def getItem(self, r, c):
            return self._data[r][c]
        def getNumRows(self):
            return self.rows
        def getNumColumns(self):
            return self.cols

    grid = GridDataStructure(3,3)
    grid.setItem(2,1,"GridTest")
    assert grid.getItem(2,1) == "GridTest"

def test_get_num_rows_cols_public():
    class GridDataStructure:
        def __init__(self, rows, cols):
            self.rows = rows
            self.cols = cols
        def getNumRows(self):
            return self.rows
        def getNumColumns(self):
            return self.cols

    grid = GridDataStructure(2,5)
    assert grid.getNumRows() == 2
    assert grid.getNumColumns() == 5