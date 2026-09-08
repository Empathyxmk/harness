def test_set_and_get_max_cards_per_row_public():
    class MaxCardsInfo:
        def __init__(self):
            self._max = 0
        def setMaxCardsPerRow(self, x):
            self._max = x
        def getMaxCardsPerRow(self):
            return self._max
    info = MaxCardsInfo()
    info.setMaxCardsPerRow(6)
    assert info.getMaxCardsPerRow() == 6