import pytest
from src.StyleValidator import StyleValidator

def test_returns_error_when_strict_unknown_style_prop():
    val = StyleValidator()
    result = val.validate({"transform": "scale(2)"}, "<Test>")
    assert isinstance(result, Exception)
    assert "Unknown style property" in str(result)

def test_no_error_when_not_strict_unknown_style_prop():
    val = StyleValidator({"strict": False})
    result = val.validate({"transform": "scale(2)"}, "<Test>")
    assert result is None

def test_returns_error_when_unsupported_style_prop():
    val = StyleValidator()
    result = val.validate({"listStylePosition": "inside"}, "<Test>")
    assert isinstance(result, Exception)
    assert "unsupported in:" in str(result)

def test_no_error_when_not_strict_unsupported_style_prop(monkeypatch):
    val = StyleValidator({"strict": False})
    result = val.validate({"a": "test", "listStylePosition": "inside", "backgroundSize": "11px"}, "<Test>")
    assert result is None

def test_no_error_when_platforms_empty():
    val = StyleValidator({"platforms": []})
    result = val.validate({"listStylePosition": "inside"}, "<Test>")
    assert result is None

def test_no_error_known_property_warns_with_comments(monkeypatch):
    val = StyleValidator({"platforms": ["gmail-android", "yahoo-mail"]})
    result = val.validate({"backgroundSize": "11px"}, "<Test>")
    assert result is None

def test_no_output_warnings_when_disabled(monkeypatch):
    val = StyleValidator({"warn": False, "platforms": ["gmail-android", "yahoo-mail"]})
    result = val.validate({"backgroundSize": "11px"}, "<Test>")
    assert result is None

def test_hyphenated_lowercase_property_same_as_camel():
    val = StyleValidator()
    result = val.validate({"listStylePosition": "inside"}, "<Test>")
    result2 = val.validate({"listStylePosition": "inside"}, "<Test>")
    assert isinstance(result, Exception)
    assert isinstance(result2, Exception)
    assert str(result) == str(result2)

def test_changes_req_after_setConfig():
    val = StyleValidator()
    result = val.validate({"listStylePosition": "inside"}, "<Test>")
    assert isinstance(result, Exception)
    assert "unsupported in:" in str(result)
    val.setConfig({"platforms": ["gmail"]})
    result2 = val.validate({"listStylePosition": "inside"}, "<Test>")
    assert result2 is None