import pytest

class DrawerAction:
    def get_line_data(self):
        # Simulates: returns 12-length array, index 5==0.5
        arr = [0.3, 0.2, 0.4, 0.1, 0.8, 0.5, 0.9, 0.7, 0.0, 0.6, 0.1, 0.3]
        return arr

def test_drawer_action_line_data():
    drawer_action = DrawerAction()
    assert drawer_action.get_line_data() is not None
    assert len(drawer_action.get_line_data()) == 12

    # check for correct center value
    assert abs(drawer_action.get_line_data()[5] - 0.5) < 0.00001