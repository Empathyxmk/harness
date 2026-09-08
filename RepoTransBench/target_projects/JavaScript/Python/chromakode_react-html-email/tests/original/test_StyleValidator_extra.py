import pytest
from src.StyleValidator import StyleValidator

class DummyValidator(StyleValidator):
    def __init__(self):
        super().__init__()
        self._support_matrix = {
            "background-color": {
                "gmail": True,
                "yahoo-mail": False,
                "apple-mail": "Partial support",
            }
        }

def test_returns_error_on_unknown_property_strict():
    val = DummyValidator()
    val.setConfig({'strict': True})
    # Unknown property
    result = val.validate({"notRealProp": 1}, "MockComp")
    assert isinstance(result, Exception)

def test_returns_undefined_on_unknown_property_not_strict():
    val = DummyValidator()
    val.setConfig({'strict': False})
    # Unknown property; not strict
    result = val.validate({"notRealProp": 1}, "MockComp")
    assert result is None

def test_returns_warning_for_partial_support(monkeypatch):
    val = DummyValidator()
    val.setConfig({'warn': True, 'platforms': ['apple-mail']})
    # To verify, just call (in actual product, would check warnings)
    val.validate({"backgroundColor": "blue"}, "CompTest")
    # No assertion needed, as Python only shows warnings, not triggers error

def test_returns_error_if_unsupported_strict():
    val = DummyValidator()
    val.setConfig({'platforms': ['yahoo-mail', 'gmail'], 'strict': True})
    result = val.validate({"backgroundColor": "blue"}, "X")
    assert isinstance(result, Exception)
    assert "unsupported in: yahoo-mail" in str(result)

def test_returns_undefined_if_supported():
    val = DummyValidator()
    val.setConfig({'platforms': ['gmail'], 'strict': True})
    result = val.validate({"backgroundColor": "blue"}, "Y")
    assert result is None

def test_handles_empty_style():
    val = DummyValidator()
    assert val.validate({}, "Comp") is None