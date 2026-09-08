def test_card_data_holder():
    class CardDataHolder:
        def __init__(self, text, cardType, position, isHeaderOrFooter, viewType):
            self.text = text
            self.cardType = cardType
            self.position = position
            self.isHeaderOrFooter = isHeaderOrFooter
            self.viewType = viewType
    holder = CardDataHolder("text", 1, 2, False, 0)
    assert holder.text == "text"
    assert holder.cardType == 1
    assert holder.position == 2
    assert holder.isHeaderOrFooter == False
    assert holder.viewType == 0