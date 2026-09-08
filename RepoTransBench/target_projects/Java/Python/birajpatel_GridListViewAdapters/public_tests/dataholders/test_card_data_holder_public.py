def test_set_and_get_card_id_public():
    class CardDataHolder:
        def __init__(self):
            self._card_id = 0
        def setCardId(self, i):
            self._card_id = i
        def getCardId(self):
            return self._card_id
    holder = CardDataHolder()
    holder.setCardId(808)
    assert holder.getCardId() == 808

def test_set_and_get_is_enabled_public():
    class CardDataHolder:
        def __init__(self):
            self._enabled = True
        def setIsEnabled(self, b):
            self._enabled = b
        def isEnabled(self):
            return self._enabled
    holder = CardDataHolder()
    holder.setIsEnabled(False)
    assert holder.isEnabled() == False

def test_set_and_get_card_public():
    class CardDataHolder:
        def __init__(self):
            self._card = None
        def setCard(self, v):
            self._card = v
        def getCard(self):
            return self._card
    holder = CardDataHolder()
    holder.setCard("testPublicCard")
    assert holder.getCard() == "testPublicCard"