import pytest

def test_switch_case_logic():
    i = 10
    result = None
    if i == 0:
        result = "case 0"
    else:
        result = "default"
    assert result == "default"

    def switch_case(x):
        if x == 0:
            switch_inner = 1
            if switch_inner == 1:
                return "nested case 1"
            else:
                return "nested default"
        else:
            return "default"

    assert switch_case(0) == "nested case 1"
    assert switch_case(1) == "default"