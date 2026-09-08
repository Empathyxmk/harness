import mammoth.conversion as conversion
import pytest

def test__element_with_path_returns_expected_tag():
    element = type("Element", (), {"tag": "p", "children": [], "attributes": {}})
    result = conversion._element_with_path([("p", {})], "hello")
    assert result.tag == "p"
    assert isinstance(result.children, list)

def test__element_with_no_path_returns_content():
    result = conversion._element_with_path([], "foo")
    assert result == "foo"

def test__element_with_multiple():
    result = conversion._element_with_path([("a", {}), ("b", {})], "foo")
    assert hasattr(result, "tag")
    assert result.children[0].tag == "b"
    assert result.children[0].children == ["foo"]

def test__element_with_attribute_in_path():
    path = [("span", {"class": "abc"})]
    result = conversion._element_with_path(path, "hi")
    assert result.tag == "span"
    assert result.attributes["class"] == "abc"

def test_converter_handles_empty_input():
    c = conversion._Converter([])
    elements = list(c.convert([]))
    assert elements == []

def test_converter_handles_non_empty_input():
    c = conversion._Converter([lambda x: x + "1", lambda x: x + "2"])
    # Each function is applied in sequence.
    data = ["a"]
    result = list(c.convert(data))
    # Should yield two processed results
    assert "1" in result[0] or "2" in result[1]

def test_converter_yield_single():
    c = conversion._Converter([lambda x: x + "A"])
    res = list(c._yield(["X"], lambda x: x + "B"))
    assert "B" in res[0]

def test_converter_repr():
    # Just exercise __repr__
    c = conversion._Converter([])
    r = repr(c)
    assert "_Converter" in r