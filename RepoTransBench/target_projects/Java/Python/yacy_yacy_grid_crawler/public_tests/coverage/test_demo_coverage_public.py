def test_add_one_public():
    class DemoCoverage:
        @staticmethod
        def addOne(x):
            return x + 1
        @staticmethod
        def subtractOne(x):
            return x - 1

    result = DemoCoverage.addOne(42)
    assert result == 43

def test_subtract_one_public():
    class DemoCoverage:
        @staticmethod
        def addOne(x):
            return x + 1
        @staticmethod
        def subtractOne(x):
            return x - 1

    result = DemoCoverage.subtractOne(12)
    assert result == 11

def test_add_one_with_negative_value_public():
    class DemoCoverage:
        @staticmethod
        def addOne(x):
            return x + 1
        @staticmethod
        def subtractOne(x):
            return x - 1

    result = DemoCoverage.addOne(-7)
    assert result == -6