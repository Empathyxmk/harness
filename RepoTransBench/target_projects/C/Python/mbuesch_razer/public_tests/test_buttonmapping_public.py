BUTTON_MAPPING_SIZE = 4

class ButtonMap:
    def __init__(self):
        self.mapping = [0] * BUTTON_MAPPING_SIZE

def test_buttonmapping_public():
    bm = ButtonMap()
    init_values = [10, 20, 30, 40]
    for i in range(BUTTON_MAPPING_SIZE):
        bm.mapping[i] = init_values[i]
    for i in range(BUTTON_MAPPING_SIZE):
        assert bm.mapping[i] == init_values[i]