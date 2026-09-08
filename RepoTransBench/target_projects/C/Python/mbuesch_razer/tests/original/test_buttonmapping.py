import pytest

BUTTON_MAPPING_SIZE = 4

class ButtonMap:
    def __init__(self):
        self.mapping = [0] * BUTTON_MAPPING_SIZE

def test_buttonmapping():
    bm = ButtonMap()
    for i in range(BUTTON_MAPPING_SIZE):
        bm.mapping[i] = i
    for i in range(BUTTON_MAPPING_SIZE):
        assert bm.mapping[i] == i