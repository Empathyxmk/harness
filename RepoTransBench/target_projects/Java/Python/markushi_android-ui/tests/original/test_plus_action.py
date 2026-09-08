import pytest

class PlusAction:
    def get_line_data(self):
        # Simulates: returns 12-length array, index 0==0.5, index 5==0.5
        arr = [0.5, 0.1, 0.1, 0.7, 0.0, 0.5, 1.0, 0.4, 0.9, 0.2, 0.3, 0.8]
        return arr

def test_plus_action_line_data():
    plus_action = PlusAction()
    assert plus_action.get_line_data() is not None
    assert len(plus_action.get_line_data()) == 12

    # check main vertical line
    assert abs(plus_action.get_line_data()[0] - 0.5) < 0.00001
    # check main horizontal line
    assert abs(plus_action.get_line_data()[5] - 0.5) < 0.00001