def test_set_and_get_row_and_column_public():
    class CardPositionInfo:
        def __init__(self):
            self._row = None
            self._col = None
        def setRow(self, r):
            self._row = r
        def setColumn(self, c):
            self._col = c
        def getRow(self):
            return self._row
        def getColumn(self):
            return self._col
    info = CardPositionInfo()
    info.setRow(7)
    info.setColumn(8)
    assert info.getRow() == 7
    assert info.getColumn() == 8