import pytest
from src.modules.bar.bar import add

def test_bar_add_two_numbers():
    assert add(2, 3) == 5

def test_bar_add_defaults():
    assert add() == 0

def test_bar_add_nan():
    with pytest.raises(ValueError, match="Invalid number"):
        add(float('nan'), 2)
    with pytest.raises(ValueError, match="Invalid number"):
        add(2, float('nan'))