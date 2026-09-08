def test_base_grid_adapter_public():
    class BaseGridAdapter:
        def __init__(self):
            self.columns = 3
            self.rows = 4
        def getCount(self):
            return 0
        def getNumOfColumns(self):
            return self.columns
        def getNumOfRows(self):
            return self.rows

    adapter = BaseGridAdapter()
    adapter.getCount()
    adapter.getNumOfColumns()
    adapter.getNumOfRows()