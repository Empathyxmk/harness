def test_set_and_get_id_public():
    class Card:
        def __init__(self):
            self._id = 0
        def setId(self, item):
            self._id = item
        def getId(self):
            return self._id

    card = Card()
    card.setId(99)
    assert card.getId() == 99

def test_set_and_get_is_enabled_public():
    class Card:
        def __init__(self):
            self._enabled = True
        def setIsEnabled(self, v):
            self._enabled = v
        def isEnabled(self):
            return self._enabled

    card = Card()
    card.setIsEnabled(False)
    assert card.isEnabled() == False

def test_set_and_get_item_public():
    class Card:
        def __init__(self):
            self._item = None
        def setItem(self, v):
            self._item = v
        def getItem(self):
            return self._item

    card = Card()
    card.setItem("publicTestObject")
    assert card.getItem() == "publicTestObject"