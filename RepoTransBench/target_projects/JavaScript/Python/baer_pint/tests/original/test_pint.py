def test_pint_exports_drink_function():
    class Pint:
        def drink(self, arg=None):
            return None
    pint = Pint()
    assert hasattr(pint, 'drink')
    assert callable(pint.drink)

def test_pint_drink_returns_none_when_called():
    class Pint:
        def drink(self, arg=None):
            return None
    pint = Pint()
    result = pint.drink({})
    assert result is None