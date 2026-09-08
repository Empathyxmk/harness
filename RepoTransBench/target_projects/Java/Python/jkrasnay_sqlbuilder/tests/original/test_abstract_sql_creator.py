import pytest

class SelectCreator:
    def __init__(self):
        self.param_idx = 0

    def allocate_parameter(self):
        param = f"param{self.param_idx}"
        self.param_idx += 1
        return param

def test_allocate_parameter():
    sc = SelectCreator()
    assert sc.allocate_parameter() == "param0"
    assert sc.allocate_parameter() == "param1"
    assert sc.allocate_parameter() == "param2"