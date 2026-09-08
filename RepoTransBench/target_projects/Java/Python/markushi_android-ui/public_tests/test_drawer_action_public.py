import pytest

class DrawerAction:
    def get_line_data(self):
        arr = [0.3, 0.2, 0.4, 0.1, 0.8, 0.5, 0.9, 0.7, 0.0, 0.6, 0.1, 0.3]
        return arr

def test_drawer_action_line_data_public():
    drawer_action = DrawerAction()
    assert drawer_action.get_line_data() is not None
    assert len(drawer_action.get_line_data()) == 12

    # check a value not checked in the original (index 7)
    val_idx7 = drawer_action.get_line_data()[7]
    assert 0.0 <= val_idx7 <= 1.0

    # ensure at least one line does NOT have 0.5f value at a new index
    assert abs(drawer_action.get_line_data()[2] - 0.5) > 0.00001