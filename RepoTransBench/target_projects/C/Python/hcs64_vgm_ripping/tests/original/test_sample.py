import pytest
from vgm_ripping.sample import add, sub

def test_add():
    assert add(1, 2) == 3
    assert add(-1, -2) == 0  # Triggers the a < 0 && b < 0 branch
    assert add(5, -2) == 3

def test_sub():
    assert sub(5, 2) == 3
    assert sub(2, 5) == -3

if __name__ == "__main__":
    pytest.main()