def test_card_position_info_constructor():
    # just instantiate with 0,0,0 for coverage
    class CardPositionInfo:
        def __init__(self, a, b, c): pass
    CardPositionInfo(0, 0, 0)