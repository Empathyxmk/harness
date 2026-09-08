import pytest
from vgm_ripping.sample import add, sub

def test_add():
    # Different input/output data from possible existing test
    assert add(10, 2) == 12          # Simple case
    assert add(-3, 7) == 4           # Negative and positive combination
    assert add(0, 0) == 0            # Zeroes
    assert add(-8, -5) == 0          # Both negative, should return 0 per logic
    assert add(15, -5) == 10         # Positive and negative

def test_sub():
    assert sub(10, 7) == 3           # Simple subtraction
    assert sub(0, 5) == -5           # Zero minus positive
    assert sub(-8, -3) == -5         # Both negative
    assert sub(22, 22) == 0          # Same numbers
    assert sub(-10, 5) == -15        # Negative minus positive

if __name__ == "__main__":
    pytest.main()
    print("All public tests passed!")