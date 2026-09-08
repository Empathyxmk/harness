def test_instantiation_public():
    class CursorGridAdapter:
        def __init__(self):
            self.columns = 4
            self.rows = 2
        def getCount(self):
            return 0
        def getNumOfRows(self):
            return self.rows
        def getNumOfColumns(self):
            return self.columns

    adapter = CursorGridAdapter()
    adapter.getCount()
    adapter.getNumOfRows()
    adapter.getNumOfColumns()