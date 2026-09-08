class Abx:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def is_positive(x):
        return x > 0

def test_add_different_values():
    assert Abx.add(7, 6) == 13
    assert Abx.add(-3, 3) == 0

def test_is_positive_different_data():
    assert Abx.is_positive(2024)
    assert not Abx.is_positive(-2025)