def test_instantiation_public():
    class ListGridAdapter:
        def __init__(self):
            self.columns = 2
            self.rows = 3
        def getCount(self):
            return 0
        def getNumOfRows(self):
            return self.rows
        def getNumOfColumns(self):
            return self.columns

    adapter = ListGridAdapter()
    adapter.getCount()
    adapter.getNumOfRows()
    adapter.getNumOfColumns()