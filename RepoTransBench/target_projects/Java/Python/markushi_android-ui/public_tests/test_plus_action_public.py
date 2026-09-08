import pytest

class PlusAction:
    def get_line_data(self):
        arr = [0.5, 0.1, 0.1, 0.7, 0.0, 0.5, 1.0, 0.4, 0.9, 0.2, 0.3, 0.8]
        return arr

def test_plus_action_line_data_public():
    plus_action = PlusAction()
    assert plus_action.get_line_data() is not None
    assert len(plus_action.get_line_data()) == 12

    # check middle point of the vertical line (different index from original)
    assert abs(plus_action.get_line_data()[1] - 0.5) > 0.00001

    # check another value in the array is within [0, 1]
    assert 0.0 <= plus_action.get_line_data()[3] <= 1.0