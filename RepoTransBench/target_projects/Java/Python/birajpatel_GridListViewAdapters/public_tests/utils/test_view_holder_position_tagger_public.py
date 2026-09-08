def test_set_and_get_position_tags_public():
    class ViewHolderPositionTagger:
        def __init__(self):
            self._row = None
            self._col = None
        def setRowPosition(self, r):
            self._row = r
        def setColumnPosition(self, c):
            self._col = c
        def getRowPosition(self):
            return self._row
        def getColumnPosition(self):
            return self._col
    tagger = ViewHolderPositionTagger()
    tagger.setRowPosition(5)
    tagger.setColumnPosition(7)
    assert tagger.getRowPosition() == 5
    assert tagger.getColumnPosition() == 7