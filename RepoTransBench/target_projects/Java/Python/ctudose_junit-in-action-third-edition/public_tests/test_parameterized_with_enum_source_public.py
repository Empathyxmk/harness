import pytest

class Colors:
    RED = 'RED'
    GREEN = 'GREEN'
    BLUE = 'BLUE'
    YELLOW = 'YELLOW'

    @classmethod
    def all(cls):
        return [cls.RED, cls.GREEN, cls.BLUE, cls.YELLOW]

def is_primary(color):
    return color in (Colors.RED, Colors.GREEN, Colors.BLUE)

@pytest.mark.parametrize("color", [Colors.RED, Colors.BLUE])
def test_is_primary_true(color):
    assert is_primary(color)

@pytest.mark.parametrize("color", [Colors.YELLOW])
def test_is_primary_false(color):
    assert not is_primary(color)