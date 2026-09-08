def test_set_and_get_row_id_public():
    class RowDataHolder:
        def __init__(self):
            self._rowid = 0
        def setRowId(self, x):
            self._rowid = x
        def getRowId(self):
            return self._rowid
    holder = RowDataHolder()
    holder.setRowId(101)
    assert holder.getRowId() == 101

def test_set_and_get_row_public():
    class RowDataHolder:
        def __init__(self):
            self._row = None
        def setRow(self, v):
            self._row = v
        def getRow(self):
            return self._row
    holder = RowDataHolder()
    holder.setRow("PublicRow")
    assert holder.getRow() == "PublicRow"