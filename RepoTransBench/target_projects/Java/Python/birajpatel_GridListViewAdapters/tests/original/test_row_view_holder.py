import pytest

class RowViewHolder:
    def __init__(self):
        self._card_view_holders = []

    def getCardViewHolders(self):
        return self._card_view_holders

def test_get_card_view_holders_initial_empty():
    holder = RowViewHolder()
    l = holder.getCardViewHolders()
    assert l is not None
    assert len(l) == 0

def test_add_item_to_card_view_holders():
    holder = RowViewHolder()
    holder.getCardViewHolders().append("abc")
    assert len(holder.getCardViewHolders()) == 1
    assert holder.getCardViewHolders()[0] == "abc"