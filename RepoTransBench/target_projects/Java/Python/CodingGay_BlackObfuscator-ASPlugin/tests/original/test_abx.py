import pytest

class Abx:
    @staticmethod
    def go():
        # Simulate logic depending on time always > 0: always True
        return True

def test_go_always_true():
    assert Abx.go()