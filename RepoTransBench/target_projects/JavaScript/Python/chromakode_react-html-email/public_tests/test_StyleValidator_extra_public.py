from src.StyleValidator import StyleValidator
import pytest

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

def test_throws_error_on_null_or_undefined_public():
    val = DummyValidator()
    with pytest.raises(TypeError):
        val.validate(None, "NullTest")
    with pytest.raises(TypeError):
        val.validate(None, "UndefinedTest")

def test_warns_on_empty_style_object_warn_mode_public():
    val = DummyValidator()
    val.setConfig({'warn': True})
    val.validate({}, "EmptyStyleTest")  # Should not warn

def test_does_not_throw_for_numeric_key_public():
    val = DummyValidator()
    val.setConfig({'strict': True})
    val.validate({100: "hello"}, "HasNumberKeyComp")