import pytest

class Card:
    def __init__(self, view=None, view_holder=None):
        self._view = view
        self._view_holder = view_holder

    def getCardView(self):
        return self._view

    def getCardViewHolder(self):
        return self._view_holder

class DummyVH:
    pass

def test_card_creation_and_getters(mocker):
    v = mocker.Mock()
    vh = DummyVH()
    card = Card(v, vh)
    assert card.getCardView() == v
    assert card.getCardViewHolder() == vh